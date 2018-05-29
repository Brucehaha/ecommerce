$( document ).ready(function() {


var stripeFormModule = $(".stripe-payment-form")
var stripeTemplate = $.templates("#stripeTemplate")
var stripeFormToken = stripeFormModule.attr('public_token')
var stripeFormNextUrl = stripeFormModule.attr('next_url')
var stripeTemplateDataContext= {
  public_token:stripeFormToken,
  next_url:stripeFormNextUrl
}
var stripeTemplateHtml = stripeTemplate.render(stripeTemplateDataContext)
stripeFormModule.html(stripeTemplateHtml)


// Create a Stripe client.
const paymentForm = $(".payment-form")
const paymentFormBtn = paymentForm.find("button")
const next_url = paymentForm.attr("next_url")
console.log("3: "+next_url)

const public_token = paymentForm.attr("public_token");
// A $( document ).ready() block.

var stripe = Stripe(public_token);

// Create an instance of Elements.
var elements = stripe.elements();
console.log(next_url)

// Custom styling can be passed to options when creating an Element.
// (Note that this demo uses a wider set of styles than the guide below.)
var style = {
  base: {
    color: '#32325d',
    lineHeight: '18px',
    fontFamily: '"Helvetica Neue", Helvetica, sans-serif',
    fontSmoothing: 'antialiased',
    fontSize: '16px',
    '::placeholder': {
      color: '#aab7c4'
    }
  },
  invalid: {
    color: '#fa755a',
    iconColor: '#fa755a'
  }
};

// Create an instance of the card Element.
var card = elements.create('card', {style: style});

// Add an instance of the card Element into the `card-element` <div>.
card.mount('#card-element');

// Handle real-time validation errors from the card Element.
card.addEventListener('change', function(event) {
  var displayError = document.getElementById('card-errors');
  if (event.error) {
    displayError.textContent = event.error.message;
  } else {
    displayError.textContent = '';
  }
});

// Handle form submission.
var form = document.getElementById('payment-form');
form.addEventListener('submit', function(event) {
  event.preventDefault();
  DoSubmit();

  stripe.createToken(card).then(function(result) {
    if (result.error) {
      // Inform the user if there was an error.
      var errorElement = document.getElementById('card-errors');
      errorElement.textContent = result.error.message;
    } else {
      // Send the token to your server.
      stripeTokenHandler(next_url, result.token);


    }
  });
});


function DoSubmit(){
  paymentFormBtn.addClass("disabled")
  paymentFormBtn.html('<i  class="fa fa-spinner fa-spin"></i>sending...')
}
function endSubmit(){
  paymentFormBtn.removeClass("disabled")
  paymentFormBtn.text('Submit')
}

function stripeTokenHandler(next_url, token){
  var paymentMethodEndpoint ='/payment-method/create/';
  //pass token id, next_url(get from template absolute_uri) to billing views
  var data = {
    "token":token.id,
  };
  $.ajax({
    data:data,
    url:paymentMethodEndpoint,
    method:"POST",
    success:function(data){

      setTimeout(function(){
        endSubmit();
      }, 1000);

      $.confirm({
        title:"Success",
        content:data.message,
        theme: "modern",
        buttons: {
          ok: function () {
             window.location.href='/cart';
         }
       },
     });


      $.alert({
        title:"Success",
        content:data.message,
        theme: "modern",
      });
      card.clear
      console.log("4 : "+next_url)
      if(next_url){
        window.location.href=next_url;

      } else {
          window.location.reload()
      }

    },
    error:function(xhr,status,error){
      console.log(xhr);
      console.log(+status);
      console.log(error);
      // // xhr,status,error
      $.confirm({
        title:"error "+xhr.status,
        content:"error: "+ xhr.responseJSON.message,
        theme: "modern",
        buttons: {
          ok: function () {
             window.location.href='/cart';
         }
       },
     });

    },
});
}
})
