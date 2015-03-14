$('.collection').click(function () {
    var collectionId = $(this).data('collection-id');
    window.location = urlFor('collection.view', {'uid': collectionId});
});
