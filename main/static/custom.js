$(document).ready(function(){
    $(".choose-size").hide();
   // show size according to selected color
    $(".choose-color").on('click',function(){
        $(".choose-color").removeClass('focused');
        $(this).addClass('focused');

        var _color=$(this).attr('data-color');

        $(".choose-size").hide();
        $(".color"+_color).show();
        $(".color"+_color).first().addClass('active');

        var _price=$(".color"+_color).first().attr('data-price');
        $(".product-price").text(_price);

    });
 
    //show the price acc to selected size
    $(".choose-size").on('click',function(){
        $(".choose-size").removeClass('active');
        $(this).addClass('active');

        var _price=$(this).attr('data-price');
        $(".product-price").text(_price);
    });
 
    $(".choose-color").first().addClass('focused'); 
    var _color=$(".choose-color").first().attr('data-color');
    var _price=$(".choose-size").first().attr('data-price');

    $(".color"+_color).show();
    $(".color"+_color).first().addClass('active');
    $(".product-price").text(_price);

    //add to cart
    $(document).on('click',".add-to-cart",function(){
        var _vm=$(this);
        var _index=_vm.attr('data-index');
        var _qty =$(".product-qty-"+_index).val();
        var _productId =$(".product-id-"+_index).val();
        var _productImage =$(".product-image-"+_index).val();
        var _productTitle =$(".product-title-"+_index).val();
        var _productPrice =$(".product-price-"+_index).text();
        
        $.ajax({
            url:'/add-to-cart',
			data:{
                'id':_productId,
                'image': _productImage,
                'qty': _qty,
                'title':_productTitle,
                'price':_productPrice
                  
            },
			dataType:'json',
			beforeSend:function(){
				_vm.attr('disabled',true);
			},
			success:function(res){
				$(".cart-list").text(res.totalitems);
				_vm.attr('disabled',false);
			}
        })

    });

    //delete item from cart
    $(document).on('click','.delete-item',function(){
		var _pId=$(this).attr('data-item');
        console.log(_pId);
		var _vm=$(this);
		// Ajax
		$.ajax({
			url:'/delete-from-cart',
			data:{
				'id':_pId,
			},
			dataType:'json',
			beforeSend:function(){
				_vm.attr('disabled',true);
			},
			success:function(res){
				$(".cart-list").text(res.totalitems);
				_vm.attr('disabled',false);
				$("#cartList").html(res.data);
			}
		});
		// End
	});

    //update item from cart
    $(document).on('click','.update-item',function(){
        var _pId = $(this).attr('data-item');
        var _pQty = $(".product-qty-"+_pId).val();
        var _vm=$(this);
        $.ajax({
            url:'/update-cart',
			data:{
                'id':_pId,
                'qty':_pQty,
            },
			dataType:'json',
			beforeSend:function(){
				_vm.attr('disabled',true);
			},
			success:function(res){
				//$(".cart-list").text(res.totalitems);
				_vm.attr('disabled',false);
                $("#cartList").html(res.data);
			}
        })
    });

    // Add wishlist
	$(document).on('click',".add-wishlist",function(){
		var _pid=$(this).attr('data-product');
		var _vm=$(this);
		// Ajax
		$.ajax({
			url:"/add-wishlist",
			data:{
				product:_pid
			},
			dataType:'json',
			success:function(res){
				if(res.bool==true){
					_vm.addClass('disabled').removeClass('add-wishlist');
				}
			}
		});
		// EndAjax
	});
	// End
});