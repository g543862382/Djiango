$(function () {
    topSwiper()
     swiper2()
});
function topSwiper() {
    var swiper = Swiper('#topSwiper',{
        direction:'horizontal',
        loop:true,
        // 如果需要分页器
        pagination: '.swiper-pagination',
        pagination:true,
        effect:'cube',
        autoplay:2000,
        autoplayDisableOnInteraction:false
    })
}
function swiper2() {
    var mySwiper = new Swiper('#swiperMenu',{
        slidesPerView:3,
        paginationsClickbale:true,
        spaceBetween:5,
        loop:false,

    })
}