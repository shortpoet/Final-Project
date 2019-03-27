$(".star.rating").click(function() {
    console.log(
      $(this)
        .parent()
        .data("stars") +
        ", " +
        $(this).data("rating")
    );
    $(this)
      .parent()
      .attr("data-stars", $(this).data("rating"));
  });
  