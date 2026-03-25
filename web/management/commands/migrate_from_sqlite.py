from django.core.management.base import BaseCommand
from django.apps import apps
from django.db import transaction, connections, IntegrityError
from django.conf import settings
import os
import shutil

class Command(BaseCommand):
    help = "Copy data from 'old' (SQLite) to 'default' (MySQL) preserving M2M. Skips Django internals by default."

    def add_arguments(self, parser):
        parser.add_argument(
            "--skip-admin",
            action="store_true",
            help="Skip Django admin and other built-in apps (default behavior).",
        )
        parser.add_argument(
            "--old-media-root",
            type=str,
            default=None,
            help="Optional path to old MEDIA_ROOT to copy files from.",
        )
        parser.add_argument(
            "--apps",
            type=str,
            default="",
            help="Comma-separated list of app labels to migrate (overrides skip-admin).",
        )

    def handle(self, *args, **options):
        src_alias = "old"
        dst_alias = "default"

        # Basic checks
        if src_alias not in settings.DATABASES:
            self.stderr.write(f"Database alias '{src_alias}' not found in settings.DATABASES. Aborting.")
            return
        if dst_alias not in settings.DATABASES:
            self.stderr.write(f"Database alias '{dst_alias}' not found in settings.DATABASES. Aborting.")
            return

        self.stdout.write("Starting migration from SQLite (old) to MySQL (default).")

        # Determine which apps to migrate
        explicit_apps = [a.strip() for a in options.get("apps").split(",") if a.strip()]
        if explicit_apps:
            models = [m for m in apps.get_models() if m._meta.app_label in explicit_apps and m._meta.managed]
        else:
            skip_admin = options.get("skip_admin", True)
            builtin = {"admin", "auth", "contenttypes", "sessions"}
            models = []
            for m in apps.get_models():
                if not m._meta.managed:
                    continue
                if skip_admin and m._meta.app_label in builtin:
                    continue
                models.append(m)

        # Ensure auth.User is copied first if present
        def model_priority(m):
            if m._meta.label_lower == "auth.user":
                return 0
            return 1
        models_sorted = sorted(models, key=model_priority)

        # Collect M2M relations for second pass
        m2m_relations = []
        for model in models_sorted:
            m2m_fields = [f for f in model._meta.many_to_many]
            if m2m_fields:
                m2m_relations.append((model, m2m_fields))

        # Helper: check referenced FK exists in destination
        def ensure_fk_value(field, val):
            if val is None:
                return None
            rel_model = field.related_model
            try:
                exists = rel_model.objects.using(dst_alias).filter(pk=val.pk).exists()
            except Exception:
                # If val is a raw PK (int) rather than model instance
                try:
                    exists = rel_model.objects.using(dst_alias).filter(pk=val).exists()
                except Exception:
                    exists = False
            return val if exists else None

        # First pass: copy concrete fields (non-M2M)
        for model in models_sorted:
            label = model._meta.label
            self.stdout.write(f"Copying model {label} ...")
            try:
                src_qs = model.objects.using(src_alias).all()
            except Exception as e:
                self.stderr.write(f"Cannot read {label} from source: {e}")
                continue

            for src_obj in src_qs:
                # Skip objects without PK
                if getattr(src_obj, "pk", None) is None:
                    self.stderr.write(f"Skipping {label} with no PK")
                    continue

                data = {}
                pk_name = model._meta.pk.name
                pk_val = getattr(src_obj, pk_name, None)

                # Build data dict for concrete fields only
                for field in model._meta.concrete_fields:
                    if field.auto_created:
                        continue
                    # For FK fields, ensure referenced object exists in destination
                    if field.is_relation and field.many_to_many is False:
                        raw_val = getattr(src_obj, field.name)
                        safe_val = ensure_fk_value(field, raw_val)
                        data[field.name] = safe_val
                    else:
                        data[field.name] = getattr(src_obj, field.name)

                # Try to create/update per-object with its own atomic block
                try:
                    with transaction.atomic(using=dst_alias):
                        # If PK present and not auto-created, try to preserve it
                        if pk_val is not None:
                            exists = model.objects.using(dst_alias).filter(pk=pk_val).exists()
                            if exists:
                                # update existing row
                                model.objects.using(dst_alias).filter(pk=pk_val).update(**{k: v for k, v in data.items() if k != pk_name})
                            else:
                                # create with explicit PK
                                obj_kwargs = {k: v for k, v in data.items()}
                                new_obj = model(**obj_kwargs)
                                try:
                                    setattr(new_obj, pk_name, pk_val)
                                except Exception:
                                    # if PK cannot be set directly, skip setting it
                                    pass
                                new_obj.save(using=dst_alias)
                        else:
                            model.objects.using(dst_alias).create(**data)
                except IntegrityError as e:
                    self.stderr.write(f"Skipping {label} pk={pk_val}: {e}")
                    continue
                except Exception as e:
                    self.stderr.write(f"Warning copying {label} pk={pk_val}: {e}")
                    continue

        # Second pass: M2M relations
        for model, m2m_fields in m2m_relations:
            label = model._meta.label
            self.stdout.write(f"Processing M2M for {label} ...")
            try:
                src_qs = model.objects.using(src_alias).all()
            except Exception as e:
                self.stderr.write(f"Cannot read {label} from source for M2M: {e}")
                continue

            for src_obj in src_qs:
                src_pk = getattr(src_obj, "pk", None)
                if src_pk is None:
                    continue
                try:
                    dst_obj = model.objects.using(dst_alias).get(pk=src_pk)
                except model.DoesNotExist:
                    continue

                for m2m_field in m2m_fields:
                    try:
                        src_related_qs = getattr(src_obj, m2m_field.name).using(src_alias).all()
                    except Exception as e:
                        self.stderr.write(f"Cannot read M2M {label}.{m2m_field.name} from source: {e}")
                        continue

                    # Clear existing relations in destination then add
                    try:
                        getattr(dst_obj, m2m_field.name).using(dst_alias).clear()
                    except Exception:
                        # If clear fails (permissions/constraints), continue to add
                        pass

                    for related in src_related_qs:
                        rel_pk = getattr(related, "pk", None)
                        if rel_pk is None:
                            continue
                        rel_model = related.__class__
                        try:
                            rel_dst = rel_model.objects.using(dst_alias).get(pk=rel_pk)
                            getattr(dst_obj, m2m_field.name).using(dst_alias).add(rel_dst)
                        except Exception as e:
                            self.stderr.write(f"Warning linking M2M {label}.{m2m_field.name} pk={rel_pk}: {e}")
                            continue

        # Copy media files if requested
        old_media = options.get("old_media_root") or getattr(settings, "OLD_MEDIA_ROOT", None)
        media_root = getattr(settings, "MEDIA_ROOT", None)
        if old_media and media_root:
            self.stdout.write("Copying media files from old media root ...")
            if os.path.isdir(old_media):
                for root, dirs, files in os.walk(old_media):
                    rel = os.path.relpath(root, old_media)
                    dst_dir = os.path.join(media_root, rel) if rel != "." else media_root
                    os.makedirs(dst_dir, exist_ok=True)
                    for f in files:
                        src_file = os.path.join(root, f)
                        dst_file = os.path.join(dst_dir, f)
                        if not os.path.exists(dst_file):
                            try:
                                shutil.copy2(src_file, dst_file)
                            except Exception as e:
                                self.stderr.write(f"Failed to copy media file {src_file}: {e}")
            else:
                self.stderr.write(f"Old media root not found: {old_media}")

        self.stdout.write(self.style.SUCCESS("Migration complete."))