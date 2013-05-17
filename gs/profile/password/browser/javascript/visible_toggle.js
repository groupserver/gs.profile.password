jQuery.noConflict();

function GSProfilePasswordToggle (entryId, toggleId) {
    var entry = null, 
        toggle = null,
        visible = false;

    function set_visible () {
        entry.attr('type', 'text');
        visible = true;
    }
    
    function set_hidden () {
        entry.attr('type', 'password');
        visible = false;
    }

    function get_visibility_value () {
        return visibile;
    }

    function toggle_visibility () {
        visible = ! visible;
        if ( visible ) {
            set_visible();
        } else {
            set_hidden();
        }
    }

    function init () {
        entry = jQuery(entryId);
        toggle = jQuery(toggleId);
        visible = Boolean(Number(toggle.val()));
        if ( visible ) {
            set_visible();
        } else {
            set_hidden();
        }
        toggle.change(toggle_visibility);
    }
    init(); // Note the automatic execution

    return {
        get_visibility: function () { return get_visibility_value(); },
    }
} // GSProfilePasswordToggle
