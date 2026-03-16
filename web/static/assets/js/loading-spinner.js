// Loading Spinner JavaScript
$(document).ready(function() {
    'use strict';

    // Add loading overlay to body
    $('body').append(`
        <div class="loading-overlay" id="pageLoadingOverlay">
            <div class="spinner"></div>
        </div>
        <div class="page-loading" id="pageLoadingBar"></div>
    `);

    // Show page loading on navigation
    $(document).on('click', 'a[href]:not([href^="#"]):not([target="_blank"]):not([href*="javascript:"])', function(e) {
        var href = $(this).attr('href');
        // Don't show loading for same page anchors or external links
        if (href && href !== '#' && !href.startsWith('javascript:') && !$(this).attr('target')) {
            showPageLoading();
        }
    });

    // Show loading on form submissions
    $(document).on('submit', 'form', function(e) {
        var $form = $(this);
        var $submitBtn = $form.find('button[type="submit"], input[type="submit"]');

        // Add loading state to submit button
        $submitBtn.addClass('btn-loading');

        // Show form overlay if form has loading-overlay class
        if ($form.hasClass('show-loading-overlay')) {
            var $overlay = $form.find('.form-loading-overlay');
            if ($overlay.length === 0) {
                $form.css('position', 'relative').append('<div class="form-loading-overlay"><div class="spinner"></div></div>');
                $overlay = $form.find('.form-loading-overlay');
            }
            $overlay.addClass('show');
        }

        // For non-AJAX forms, show page loading
        if (!$form.hasClass('ajax-form')) {
            showPageLoading();
        }
    });

    // Handle AJAX form submissions
    $(document).on('submit', 'form.ajax-form', function(e) {
        e.preventDefault();
        var $form = $(this);
        var $submitBtn = $form.find('button[type="submit"], input[type="submit"]');

        $submitBtn.addClass('btn-loading');

        // Show form overlay
        var $overlay = $form.find('.form-loading-overlay');
        if ($overlay.length === 0) {
            $form.css('position', 'relative').append('<div class="form-loading-overlay"><div class="spinner"></div></div>');
            $overlay = $form.find('.form-loading-overlay');
        }
        $overlay.addClass('show');

        // Submit form via AJAX
        var formData = new FormData($form[0]);
        $.ajax({
            url: $form.attr('action') || window.location.href,
            type: $form.attr('method') || 'POST',
            data: formData,
            processData: false,
            contentType: false,
            success: function(response) {
                // Handle success - you might want to redirect or show a message
                if (response.redirect) {
                    window.location.href = response.redirect;
                } else {
                    hideLoading();
                    // Show success message or handle response
                }
            },
            error: function(xhr, status, error) {
                hideLoading();
                // Handle error - show error message
                console.error('Form submission error:', error);
            }
        });
    });

    // Show page loading
    window.showPageLoading = function() {
        $('#pageLoadingOverlay').addClass('show');
        $('#pageLoadingBar').addClass('show');
    };

    // Hide all loading states
    window.hideLoading = function() {
        $('#pageLoadingOverlay').removeClass('show');
        $('#pageLoadingBar').removeClass('show');
        $('.btn-loading').removeClass('btn-loading');
        $('.form-loading-overlay').removeClass('show');
    };

    // Hide loading on page load
    $(window).on('load', function() {
        hideLoading();
    });

    // Hide loading when page becomes visible (in case of back/forward navigation)
    $(document).on('visibilitychange', function() {
        if (!document.hidden) {
            hideLoading();
        }
    });

    // Auto-hide loading after 10 seconds as fallback
    setTimeout(function() {
        hideLoading();
    }, 10000);
});