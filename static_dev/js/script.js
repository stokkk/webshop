"user strict"


const ratings = document.querySelectorAll('.rating-star');
if (ratings.length > 0) {
    initRatings();
}

function initRatings() {
    let ratingActive, ratingValue;
    for (let index = 0; index < ratings.length; index++) {
        const rating = ratings[index];
        initRating(rating);
    }

    function initRating(rating) {
        initRatingVars(rating);
        setActiveRatingWidth();

        if (rating.classList.contains('not-static')) {
            setRating(rating);
        }
    }

    function initRatingVars(rating) {
        ratingActive = rating.querySelector('.rating__active');
        ratingValue = rating.querySelector('.rating__value');
    }

    function setActiveRatingWidth(index = ratingValue.innerHTML) {
        const ratingActiveWidth = index / 0.05;
        ratingActive.style.width = `${ratingActiveWidth}%`;
        ratingValue.nextElementSibling.value = index;
    }
    
    function setRating(rating) {
        const ratingItems = rating.querySelectorAll('.rating__item');
        for (let index = 0; index < ratingItems.length; index++) {
            const ratingItem = ratingItems[index];
            ratingItem.addEventListener("mouseenter", function(e) {
                initRatingVars(rating);

                setActiveRatingWidth(ratingItem.value);
                
            });
            ratingItem.addEventListener("mouseleave", function(e) {
                setActiveRatingWidth();
            });
            ratingItem.addEventListener("click", function (e) {
                initRatingVars(rating);
                ratingValue.innerHTML = index + 1;
                setActiveRatingWidth();
            })
        }
    }

}



function showMsg() {
    var spans = $.find('#msg span');
    if (spans.length > 0) {
        var msgText = spans[0].textContent;
        var msgType = spans[1].textContent;
        var msgPlace = spans[2].textContent;
        var divMsg = document.getElementById(msgPlace);
        var parentElement = divMsg.parentNode;
        var msgBlock = document.createElement("div");
        if (msgType == "info") {
            msgBlock.className = "info success";
        } else if (msgType == "error") {
            msgBlock.className = "info failure";
        }
        p = document.createElement("p");
        p.textContent = msgText;
        msgBlock.appendChild(p);
        parentElement.insertBefore(msgBlock, divMsg);
    } 
}
// showMsg();

function hideMsgBlock() {
    var info = $.find('.info')[0];
    if (info) {
        info.style.opacity = '0';
        setTimeout(info.remove, 5000);
    }
}
setTimeout(hideMsgBlock, 3000);
