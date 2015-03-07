// Flash message
setTimeout(showFlash, 200);
setTimeout(hideFlash, 2000);


// get random num which >= start and <= end
function rangeBetween(start, end) {
    return Math.floor(Math.random() * (end - start + 1) + start);
}

// get random item from array
function getRandomItem(array) {
    var randomIndex = rangeBetween(0, slogans.length - 1);
    return array[randomIndex];
}

var slogans = [
    '经典，不惧火炼。',
    '经典，时间考验。',
    '经典，常读常新。',
    '经典，经久不衰。'
];

// display random footer slogan
$('.footer-slogan').text(getRandomItem(slogans));

/**
 * Show flash message.
 */
function showFlash() {
    $('.flash-message').slideDown('fast');
}

/**
 * Hide flash message.
 */
function hideFlash() {
    $('.flash-message').slideUp('fast');
}
