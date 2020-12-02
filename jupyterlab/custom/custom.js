define([
    'base/js/namespace',
    'base/js/promises',
    'base/js/events'
], function (Jupyter, promises, events) {

    promises.app_initialized.then(function (appname) {
        // hide header and view menu if in iframe
        $("#login_widget").hide();
        $("#login_widget + span").hide();
        $("#shutdown").hide();

        if (appname === 'DashboardApp') {
            // hide clusters tab
            $(".clusters_tab_link").parent().hide();
        }

        if (appname === 'NotebookApp') {
            // hide header and view menu if in iframe
            if (inIframe()) {
                $('body').addClass('in-inframe');
                $("#view_menu").closest(".dropdown").hide();
                $("#header-container").hide();
                $("#header .header-bar").hide();
                $("#menubar-container").css({'width':'auto', 'max-width':'1140px'});
            }

            // Fix kernel logo margin
            $("#kernel_logo_widget").css("margin","0");

            // hide unecessary menus
            $("#help_menu").closest(".dropdown").hide();
            $("#notification_area").hide();
            $("#kernel_indicator").hide();
            $("#modal_indicator").hide();
            $("#move_up_down").hide();
            $("#cmd_palette").hide();
            $("#new_notebook").hide();
            $("#open_notebook").hide();
            $("#open_notebook + .divider").hide();
            $("#copy_notebook").hide();
            $("#save_notebook_as").hide();
            $("#rename_notebook").hide();

            // rephrase the 'checkpoint' thing that is confusing
            $("#save_checkpoint>a").html("Save");
            $('button[title="Save and Checkpoint"]').attr('title', 'Save');

            promises.notebook_loaded.then(function () {
            });

            // hide widget menu
            events.on('kernel_ready.Kernel', function () {
                $("#widget-submenu").closest(".dropdown").hide();
            });
        }
    });

    function inIframe () {
        try {
            return window.self !== window.top;
        } catch (e) {
            return true;
        }
    }
});

// Make custom url to remove user id in url
var pattern = /user\/[a-zA-Z0-9]+\//g;
var url = window.location.href.replace(pattern, "user/");
// Matomo tracking analytics
var _paq = _paq || [];
_paq.push(['setCustomUrl', url]);
_paq.push(['trackPageView']);
_paq.push(['enableLinkTracking']);
(function () {
    var u = "//piwik.inria.fr/";
    _paq.push(['setTrackerUrl', u + 'piwik.php']);
    _paq.push(['setSiteId', '87']);
    var d = document, g = d.createElement('script'), s = d.getElementsByTagName('script')[0];
    g.type = 'text/javascript';
    g.async = true;
    g.defer = true;
    g.src = u + 'piwik.js';
    s.parentNode.insertBefore(g, s);
})();
