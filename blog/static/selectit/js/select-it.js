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

(function($) {
	$.widget(
		// name
		'ui.selectit',

		// base
		{
			options: {
				availableSelection: []
			},

			_checkAdded: function(newSelect) {
				for (var i = 0; i < this.options.availableSelection.length; ++i) {
					if (newSelect == this.options.availableSelection[i])
						return true;
				}

				return false;
			},

			_create: function() {
				this.$selections = $('<select id="sel1"></select>').appendTo(this.element);
				$('<div id="add_dialog" title="Add Catalog">' +
					'<form>' +
					'<fieldset>' +
					'<label for="name">Name</label>' +
					'<input type="text" name="name" id="name">' +
					'</fieldset>' +
					'</form>' +
					'</div>').appendTo(this.element).hide();

				var name = $("#name");

				var value = 1;
				for (var i = 0; i < this.options.availableSelection.length; ++i) {
					this.$selections.append('<option value =\"' + i + '\">' + this.options.availableSelection[i] + '</option>');
				}

				this.$selections.append('<option id="add_selection" value =\"100\"> + </option>');

				$("#sel1").on('change', {selecit: this, added: name, $selections: this.$selections}, function(event) {
					$("#sel1 option:selected").each(function() {
						if ($(this).attr("id") == "add_selection") {
							$('#add_dialog').dialog({
								height: 300,
								width: 350,
								modal: true,
								buttons: {
									"Confirm": function() {
										if (event.data.selecit._checkAdded(event.data.added.val())) {
											alert(event.data.added.val() + "has been added!");
										} else {
											event.data.$selections.prepend(
													'<option value ="' +
													event.data.$selections.children().length +
													'\">' +
													event.data.added.val() +
													'</option>');
											event.data.$selections.children().first().attr("selected", true);
										}

										$(this).dialog("close");
									},

									Cancel: function() {
										$(this).dialog("close");
									}
								}
							});
						}
					});
				});
			}
		}
	);
})(jQuery);
