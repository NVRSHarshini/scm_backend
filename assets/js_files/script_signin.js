const switchers = [...document.querySelectorAll('.switcher')]

switchers.forEach(item => {
	item.addEventListener('click', function() {
		switchers.forEach(item => item.parentElement.classList.remove('is-active'))
		this.parentElement.classList.add('is-active')
	})
})
gapi.load('auth2', function () {
    gapi.auth2.init({
      client_id: '37099103882-oamqfkog57m563c9t5r3k7e8gg5sg90s.apps.googleusercontent.com',
    });
  });
  
  // Trigger Google Sign-In when a user clicks a login button
  document.querySelector('#google-login-btn').addEventListener('click', function () {
    gapi.auth2.getAuthInstance().signIn().then(function (googleUser) {
      const profile = googleUser.getBasicProfile();
      const idToken = googleUser.getAuthResponse().id_token;
    });
});