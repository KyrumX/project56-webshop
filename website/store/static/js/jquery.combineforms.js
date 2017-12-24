$(document).ready(function () {
    console.log("Hello worlddd");
});

$("form").submit(function () {
    console.log("Inside function...");
    combineForms();
    return false;
});

function combineForms() {
    console.log("in combineForms");
    var $newForm = $("<form></form>")
        .attr({method: "GET", action : ""});

    $('form[name="orderform"], form[name="filterform"] :input:not(:submit, :button) :checkbox(:checked)').each(function () {
        console.log(this.name);
        $newForm.append($("<input type=\"hidden\" />")
            .attr('name', this.name)
            .val($(this).val())
        );
    });

    // $(':input:not(:submit, :button)').each(function () {
    //     $newForm.append($("<input type=\"hidden\" />")
    //         .attr('name', this.name)
    //         .val($(this).val())
    //     );
    // });
    $newForm
        .appendTo(document.body)
        .submit();
}

    // $('form:not([name="searchForm"]) :input').each(function () {
    //    $newForm.append($("<input type=\"hidden\" />")
    //         .attr('name', this.name)
    //         .val($(this).val())
    //      );
    // });


    // $('form[name="orderform"], form[name="filterform"] :input:not(:submit, :button, :not(:checked))').each(function () {
    //     console.log(this.name);
    //     $newForm.append($("<input type=\"hidden\" />")
    //         .attr('name', this.name)
    //         .val($(this).val())
    //     );
    // });