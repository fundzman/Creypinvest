(function($) {
	$(document).ready(function() {

		// Card Shuffle 
		function sortCards() {
			var cards = $('.account:not(.is-selected)', '.my-wallet-sidebar'),
				i = 0;
			
			$('.is-stationary').removeClass('is-stationary');
			
			cards.each(function(i) {
				var index = i;

				$(this).css({
					'top': (180 / (cards.length-1)) * index + 'px'
				});
				
				i++;
				
				if( cards.length === i || cards.length <= 2 ) {
					$(this).addClass('is-stationary');
				}
			});// END each
		}
		
		sortCards();
	
		// Set active account
		$(document).on('click','.my-wallet-sidebar .account:not(.is-selected)', function() {
			var card = $(this),
				account = $('[data-account="' + $(this).attr('data-account') +'"]'),
				selected = $('.is-selected'),
				placeholder = $('.transaction-history-placeholder');
			
			account.addClass('is-selected'); 
			placeholder.addClass('is-hidden');
			selected.removeClass('is-selected');
			setTimeout( sortCards, 10);
		});
		
		// Add Account
		$('.account-number').mask('9999 9999 9999 9999', {placeholder:'**** **** **** ****'});
		$.mask.definitions['a']='';
		$('.account-expiration').mask('Valid Thru: 99/99');
		
		// Modal
		$('.add-account').on('click', function() {
			$('.add-account-modal').addClass('is-visible');
		});
		
		function addAccount() {
			var accountNum = $('input.account-number').val(),
				accountExp = $('input.account-expiration').val(),
				cardType = $('.account-card-type.is-selected').attr('data-card-type'),
				accountsContainer = $('.accounts-container'),
				html,
				htmlHistory;
			
			html = '<div class="account" data-account="' + accountNum.substr(15) + '">'
				 + '<div class="account-card-type ' + cardType + '"></div>'
				 + '<div class="account-number">**** **** **** ' + accountNum.substr(15) + '</div>'
				 + '<div class="account-expiration">' + accountExp + '</div>'
				 + '</div><!-- /.account -->'; 
			
			htmlHistory = '<div class="account-details" data-account="' + accountNum.substr(15) + '"><div class="account-balance">Current Balance<div class="value-unit">$0.<sup class="value-subunit">00</sup><!-- /.subunit --></div><!-- /.unit --></div><!-- /.account-balance --><div class="temp-account">Pending New Account</div></div><!-- /.account --></div><!-- /.account-details -->';
			
			if( accountNum != '' && accountExp != '' ) {
				accountsContainer.append(html);
				$('.account-details-container').append(htmlHistory);
				$('input.account-number, input.account-expiration').val('');
				$('.add-account-modal').removeClass('is-visible');
			} else {
				$('.new-account').addClass('has-error');
				setTimeout( function() {
					$('.new-account').removeClass('has-error');
				}, 400);
			}
		}
		
		var addAccountButton = $('.new-account button');
		
		addAccountButton.on('click', function() {
			addAccount();
			sortCards();
		});
		
		// Close modal on overlay click
		$('.add-account-modal .overlay').on('click', function () {
			$('.add-account-modal').removeClass('is-visible');
		});
		
		// Select card type
		$('.new-account .account-card-type').on('click',function() {
			$('.account-card-type.is-selected').removeClass('is-selected');
			$(this).addClass('is-selected');
		});
		
	});
})(jQuery);


