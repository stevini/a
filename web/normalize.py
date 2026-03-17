from web.models import Products
p = Products.objects.all()
try:
    for i in p:              
        i.name = i.name.capitalize()
        i.save()         
        print(f'{i}updated')
except:
    print(f'error at {i}')
