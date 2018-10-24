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

function toggleProfileModal()
{
    $("#profileModal").fadeToggle();
    console.log("Toggle Profile Modal");
}

function login()
{
    console.log($("#loginForm").serialize());
    $.ajax({
        type: "POST",
        url: "/login",
        data: $("#loginForm").serialize(),
        success: function(response){
            if(response['Flag']) {
                $("#loginModalBtn").hide();
                $("#signupModalBtn").hide();
                $("#profileBtn").show();
                $("#profileBtn").html('<i class="fa fa-user-circle"></i> '+ response['Name']);
                $("#profileForm input[name='Name']").val(response['Name']);
                $("#profileForm input[name='Age']").val(response['Age']);
                $("#profileForm input[name='Email']").val(response['Email']);
                email = response['Email'];
                toggleLoginModal();
                console.log("Login Successful!");
            }
            else {
                console.log("Login Failed!");
            }
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
            console.log(response['Message'])
        }
    });
}

$("#saveBtn").click(function () {
    changeInfo();
});
$("#logoutBtn").click(function () {
    logout();
});

function changeInfo()
{
    $.ajax({
        type: "POST",
        url: "/changeinfo",
        data: $("#profileForm").serialize();,
        success: function (response) {
            if(response['Flag']) {
                $("#profileBtn").html('<i class="fa fa-user-circle"></i> '+ response['Name']);
                $("#profileForm:input[name='Name']").html(response['Name']);
                $("#profileForm:input[name='Age']").html(response['Age']);
                $("#profileForm:input[name='Email']").html(response['Email']);
                console.log("Changes Successful!");
            }
            else {
                console.log("Changes failed!");
            }
        }
    });
}


function logout()
{
    $.ajax({
        type: "POST",
        url: "/logout",
        success: function (response) {
            console.log(response);
        }
    });
    $("#loginModalBtn").show();
    $("#signupModalBtn").show();
    $("#profileModal").fadeOut();
    $("#profileBtn").hide();
    $("#profileBtn").html();
    $("#profileForm input").val();

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
$("#profileBtn").click(function () {
   toggleProfileModal();
});
