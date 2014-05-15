/*
 * jQuery UI select-it!
 *
 * Authors:
 *   Yangtianhang(tianhang.yang@gmail.com)
 *
 * Maintainer:
 *   Yangtianhang(tianhang.yang@gmail.com)
 *
 * Dependencies:
 */

(function ($) {
    // utility functions (won’t be inherited)
    function foo() {
    }

    $.widget('ui.selecit', {
        options: {
            availableOption: []
        },

        _create: function () {
            var that = this;
            this.selectElement = "";

        }
    });
})(jQuery);
