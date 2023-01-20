$(document).ready(() => {
  $('form').submit(function (e) {
    e.preventDefault();
  
    $('#loading').show();
    $('#btn-convert').addClass('cursor-not-allowed');
    $('#btn-convert').prop('disabled', true);
    
    var url = $('#url').val();
  
    if (!url.length) {
      alert('Please enter a YouTube URL');
      return;
    }
  
    // Check if URL is valid
    if (!url.match(/^(http(s)?:\/\/)?((w){3}.)?youtu(be|.be)?(\.com)?\/.+/)) {
      alert('Please enter a valid YouTube URL');
      return;
    }
  
    var csrfToken = $('input[name="csrf_token"]').val();
    var filename = '';
  
    fetch('/download', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': csrfToken
      },
      body: JSON.stringify({
        url: url,
      })
    })
    .then(res => {
      // response headers
      res.headers.forEach((value, name) => {
        console.log(name, value);
      });
      
      if (!res.ok) {
        throw new Error('Network response was not ok');
      }

      if (!res.headers.get('content-disposition')) {
        throw new Error('No content-disposition header');
      }
  
      filename = res.headers.get('content-disposition').split('filename=')[1];
      if (!filename) {
        throw new Error('No filename');
      }
      
      return res.blob();
    })
    .then(blob => {
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.style.display = 'none';
      a.href = url;
      a.download = filename;
      document.body.appendChild(a);
      a.click();
      window.URL.revokeObjectURL(url);
    })
    .catch(err => {
      alert(err.message);
    })
    .finally(() => {
      $('#loading').hide();
      $('#btn-convert').removeClass('disabled cursor-not-allowed');
      $('#btn-convert').prop('disabled', false);
    });
  });
  
});
