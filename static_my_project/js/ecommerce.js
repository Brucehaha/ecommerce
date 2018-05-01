$(document).ready(function(){

// submit contact details
  var contactForm = $(".contact-form");
  var contactFormMethod = contactForm.attr("method");
  var contactFormEndpoint = contactForm.attr("action");
  var contactFormBtn = contactForm.find("[type='submit']");
  var contactFormData = contactForm.serialize();

  function DoSubmit(){
    contactFormBtn.addClass("disabled")
    contactFormBtn.html('<i  class="fa fa-spinner fa-spin"></i>sending...')
  }
  function endSubmit(){
    contactFormBtn.removeClass("disabled")
    contactFormBtn.text('Submit')
  }

  contactForm.submit(function(event){
    event.preventDefault()
    DoSubmit()
    var contactFormData = contactForm.serialize();
    $.ajax({
      method: contactFormMethod,
      url: contactFormEndpoint,
      data: contactFormData,
      success: function(data){
        console.log(contactForm)
        setTimeout(function(){
          endSubmit()
        }, 2000)
        setTimeout(function(){
          $.alert({
            title:"Success",
            content:data.message,
            theme: "modern",
          })
        }, 2000)
        contactForm[0].reset()
      },
      error: function(error){
        console.log(error.responseJSON)
         endSubmit()
        var msg="";
        var jsonError = error.responseJSON;
        $.each(jsonError, function(key, value){
          msg += key + ": " + value[0].message+"<br/>";
        })
        $.alert({
          title:"Oops",
          content: msg,
          theme: "modern",
        })
      },
    })
  })

// search form loading product when keyup
  var searchForm =$(".search-form");
  var searchFormInput = searchForm.find("[name='q']");
  var searchFormBtn = searchForm.find("[type='submit']");
  var typingTimer;
  var searchTimer;

  searchFormInput.keyup(function(event){
    clearTimeout(typingTimer)

    typingTimer = setTimeout(productSearch, 500);

  })

  function productSearch(){
    productSearching();
    setTimeout(function(){
      window.location.href="/search/?q="+searchFormInput.val()
    }, 1000)

  }

  function productSearching(){
    searchFormBtn.addClass("disabled")
    searchFormBtn.html('<i  class="fa fa-spinner fa-spin"></i>Search...')
  }



// cart update button js
  var productForm = $(".form-product-ajax")

  productForm.submit(function(event){
    event.preventDefault();
    var thisForm = $(this);
    // var actionEndpoint = thisForm.attr("action");
    var actionEndpoint = thisForm.attr("data-endpoint"); //api endpoint
    var httpMethod = thisForm.attr("method");
    var formData = thisForm.serialize();
    console.log(formData)


    $.ajax({
      url: actionEndpoint,
      method:httpMethod,
      data: formData,
      success: function(newdata){
        console.log("Added", newdata.added);
        console.log("Removed", newdata.removed);
        var submitSpan = thisForm.find(".submit-span");
        if (newdata.added){
          submitSpan.html('In Cart<button class="btn btn-link" type="submit">remove?</button>');
        } else {
          submitSpan.html('<button class="btn btn-outline-success" type="submit">Add to cart</button>');
        }
        var itemCount = $(".itemCount");
        itemCount.text(newdata.itemCount);
        if(window.location.href.indexOf("cart") != -1){
          refreshCart();
        };
      },
      error: function(errorData){
        alert("An Error Occured")
        console.log("error")
        console.log(errorData)
      },
    })
  })


// cart refresh when remove item

  function refreshCart(){
    var cartBody = $(".cartBody")
    // var cartList = cartBody.find(".cartList")
    var subtotal = $(".subtotal")
    var total = $(".total")

     $.ajax({
        url: "/api/cart/",
        method: "GET",
        success: function(data){
          var removeForm = $(".remove-form");
          var length = data.products.length;

          if (length > 0){
            cartBody.html(" ");
            i = length
            $.each(data.products, function(index, value){
              var productRemoveForm  = removeForm.clone();
              productRemoveForm.find(".product_id").val(value.id);
              console.log(productRemoveForm.html());
              cartBody.prepend('<tr><th scope="row">'+ i +'</th><td><a href="'+value.url+'">'+value.name+'</a>'+productRemoveForm.html()+'</td><td>'+value.price+'</td></tr>')
              i--
            });
            total.text(data.total);
            subtotal.text(data.subtotal);
          } else {
           console.log("else ");
           console.log(window.location.href);
           window.location.href='./';
          }
        },

       error: function(errorData){
        alert("An Error Occured")
        console.log("error")
        console.log(errorData)
      },
     })
    }
  })
