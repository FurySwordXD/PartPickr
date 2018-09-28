function toggleLoginModal()
{
    $("#loginModal").fadeToggle();
    console.log("Toggle Login Modal");
}

function toggleSignupModal()
{
    $("#signupModal").fadeToggle();
    console.log("Toggle Sign up Modal");
}

function login()
{
    console.log($("#loginForm").serialize());
    $.ajax({
        type: "POST",
        url: "/login",
        data: $("#loginForm").serialize(),
        success: function(response){
            console.log(response)
        }
    });
}

function signup()
{
    console.log($("#signupForm").serialize());
    $.ajax({
        type: "POST",
        url: "/register",
        data: $("#signupForm").serialize(),
        success: function(response){
            console.log(response)
        }
    });
}

$("#signupModalBtn").click(function () {
    toggleSignupModal();
});
$("#loginModalBtn").click(function () {
    toggleLoginModal();
});
$("#signupBtn").click(function () {
    signup();
});
$("#loginBtn").click(function () {
    login();
});