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
	$.widget(
		// name
		'ui.selectit',

		// base
		{
			options: {
				availableSelection: []
			},

			_create: function () {
				this.selections = $('<selections></selections>').insertAfter(this.element);
				var value = 1;
				for (var i = 0; i < this.options.availableSelection.length; ++i) {
					this.selections.append('<option value =\"' + i + '\">' + this.options.availableSelection[i] + '</option>');
				}
			}
		}
	);
})(jQuery);

