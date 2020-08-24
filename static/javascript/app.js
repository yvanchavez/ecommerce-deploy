

const navSlide = () => {
    const burger = document.querySelector('.burger');
    const nav = document.querySelector('.nav-links');
    const navLinks =document.querySelectorAll('.nav-links li');



    burger.addEventListener('click',()=>{
        //Toggle nav
        nav.classList.toggle('nav-active');

        //Animate links
        navLinks.forEach((link,index)=>{
            if(link.style.animation){
                link.style.animation = '';
            }else {
                link.style.animation= `navLinkFade 0.5s ease forwards ${index/7+0.5}s`;
            }

        })

        //Burger Animation
        burger.classList.toggle('toggle');
    });



}

navSlide();

//js for product gallery
//var productImg = document.getElementById("product-img");
//var smallImg = document.getElementsByClassName("small-img");
//
//smallImg[0].onclick = function()
//{
//    productImg.src= smallImg[0].src;
//}
//smallImg[1].onclick = function()
//{
//    productImg.src= smallImg[1].src;
//}
//smallImg[2].onclick = function()
//{
//    productImg.src= smallImg[2].src;
//}
////

var updateBtns = document.getElementsByClassName('update-cart')

for (i = 0; i < updateBtns.length; i++) {
	updateBtns[i].addEventListener('click', function(){
		var productId = this.dataset.product
		var action = this.dataset.action
		console.log('productId:', productId, 'Action:', action)
		console.log('USER:', user)

		if (user == 'AnonymousUser'){
			addCookieItem(productId, action)

		}else{
			updateUserOrder(productId, action)
		}
	})
}


function addCookieItem(productId, action){
	console.log('User is not authenticated')
    if (action == 'add'){
		if (cart[productId] == undefined){
		cart[productId] = {'quantity':1}

		}else{
			cart[productId]['quantity'] += 1
		}
	}

	if (action == 'remove'){
		cart[productId]['quantity'] -= 1

		if (cart[productId]['quantity'] <= 0){
			console.log('Item should be deleted')
			delete cart[productId];
		}
	}
	console.log('CART:', cart)
	document.cookie ='cart=' + JSON.stringify(cart) + ";domain=;path=/"

	location.reload()

}


function updateUserOrder(productId, action){
	console.log('User is authenticated, sending data...')

		var url = '/update_item/'

		fetch(url, {
			method:'POST',
			headers:{
				'Content-Type':'application/json',
				'X-CSRFToken':csrftoken,
			},
			body:JSON.stringify({'productId':productId, 'action':action})
		})
		.then((response) => {
		   return response.json();
		})
		.then((data) => {
		    location.reload()
		});
}

