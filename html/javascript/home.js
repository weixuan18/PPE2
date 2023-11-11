let navbarItems = document.querySelectorAll('.item');
for(let i=0; i<navbarItems.length; i++){
    navbarItems[i].addEventListener('click', function(){
        for (let i=0; j<navbarItems.length; j++){
            navbarItems[i].classList.remove('active');
        }
        this.classList.add('active');
    });
}

var typed = new Typed('.multiple-text', {
    strings:['Xinhao ZHANG', 'Yidi HUANG', 'Weixuan CHENG'],
    typeSpeed: 70,
    backSpeed: 70,
    backDelay: 900,
    loop: true
});
