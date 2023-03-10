$(document).ready(() => {
  $('form').submit(function (e) {
    e.preventDefault();

    var url = $('#url').val();
    var host_url = $('[name="host_url"]').val();

    if (!url.length) {
      alert('Please enter a YouTube URL');
      return;
    }

    // Check if URL is valid
    if (!utils.isValidUrl(url)) {
      alert('Please enter a valid YouTube URL');
      return;
    }
  
    $('#loading').show();
    $('#btn-convert').addClass('cursor-not-allowed');
    $('#btn-convert').prop('disabled', true);
  
    var csrfToken = $('input[name="csrf_token"]').val();
    // var filename = '';
  
    fetch('/convert', {
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
      if (!res.ok) {
        throw new Error(res.statusText);
      }

      // The commented code below is an example of how to get the filename from the content-disposition header
      // when we want to convert and serve files from the server.

      /*
      if (!res.headers.get('content-disposition')) {
        throw new Error('No content-disposition header');
      }
  
      filename = res.headers.get('content-disposition').split('filename=')[1];
      if (!filename) {
        throw new Error('No filename');
      }

      return res.blob();
      */

      return res.json();
    })
    .then(async res => {
      const filename = res.filename;
      const extractor = res.extractor;

      // const blob = await fetch(host_url + '/proxy/' + res.audio_url).then(r => r.blob());
      // const url = window.URL.createObjectURL(blob);
      const url = res.audio_url;

      const a = document.createElement('a');
      a.style.display = 'none';
      a.href = url;
      a.download = filename;
      a.target = '_blank';
      document.body.appendChild(a);
      a.click();
      window.URL.revokeObjectURL(url);

      const toast = document.createElement('div');
      const randomId = utils.makeId(8);
      toast.innerHTML = `
        <div id="${randomId}" class="flex items-center w-full max-w-xs p-4 text-gray-500 bg-white rounded-lg shadow dark:text-gray-400 dark:bg-gray-800" role="alert">
          <div class="inline-flex items-center justify-center flex-shrink-0 w-8 h-8 text-blue-500 bg-blue-100 rounded-lg dark:bg-blue-800 dark:text-blue-200">
            <svg aria-hidden="true" class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg"><path fill-rule="evenodd" d="M12.395 2.553a1 1 0 00-1.45-.385c-.345.23-.614.558-.822.88-.214.33-.403.713-.57 1.116-.334.804-.614 1.768-.84 2.734a31.365 31.365 0 00-.613 3.58 2.64 2.64 0 01-.945-1.067c-.328-.68-.398-1.534-.398-2.654A1 1 0 005.05 6.05 6.981 6.981 0 003 11a7 7 0 1011.95-4.95c-.592-.591-.98-.985-1.348-1.467-.363-.476-.724-1.063-1.207-2.03zM12.12 15.12A3 3 0 017 13s.879.5 2.5.5c0-1 .5-4 1.25-4.5.5 1 .786 1.293 1.371 1.879A2.99 2.99 0 0113 13a2.99 2.99 0 01-.879 2.121z" clip-rule="evenodd"></path></svg>
            <span class="sr-only">Fire icon</span>
          </div>
          <div class="ml-3 text-sm font-normal">${res.title}</div>
          <button type="button" class="ml-auto -mx-1.5 -my-1.5 bg-white text-gray-400 hover:text-gray-900 rounded-lg focus:ring-2 focus:ring-gray-300 p-1.5 hover:bg-gray-100 inline-flex h-8 w-8 dark:text-gray-500 dark:hover:text-white dark:bg-gray-800 dark:hover:bg-gray-700" data-dismiss-target="#${randomId}" aria-label="Close">
            <span class="sr-only">Close</span>
            <svg aria-hidden="true" class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg"><path fill-rule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clip-rule="evenodd"></path></svg>
          </button>
        </div>
      `;

      $('#toast-container').append(toast);
      setTimeout(() => {
        toast.remove();
      }, 3000);
    })
    .catch(err => {
      console.error(err);

      const toast = document.createElement('div');
      const randomId = utils.makeId(8);
      toast.innerHTML = `
        <div id="${randomId}" class="flex items-center w-full max-w-xs p-4 mb-4 text-gray-500 bg-white rounded-lg shadow dark:text-gray-400 dark:bg-gray-800" role="alert">
          <div class="inline-flex items-center justify-center flex-shrink-0 w-8 h-8 text-red-500 bg-red-100 rounded-lg dark:bg-red-800 dark:text-red-200">
            <svg aria-hidden="true" class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg"><path fill-rule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clip-rule="evenodd"></path></svg>
            <span class="sr-only">Error icon</span>
          </div>
          <div class="ml-3 text-sm font-normal">${(err.message.length > 200) ? `${err.message.substring(0, 200)}...` : err.message}</div>
          <button type="button" class="ml-auto -mx-1.5 -my-1.5 bg-white text-gray-400 hover:text-gray-900 rounded-lg focus:ring-2 focus:ring-gray-300 p-1.5 hover:bg-gray-100 inline-flex h-8 w-8 dark:text-gray-500 dark:hover:text-white dark:bg-gray-800 dark:hover:bg-gray-700" data-dismiss-target="#${randomId}" aria-label="Close">
            <span class="sr-only">Close</span>
            <svg aria-hidden="true" class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg"><path fill-rule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clip-rule="evenodd"></path></svg>
          </button>
        </div>
      `;

      $('#toast-container').append(toast);
      setTimeout(() => {
        toast.remove();
      }, 3000);
    })
    .finally(() => {
      $('#loading').hide();
      $('#btn-convert').removeClass('disabled cursor-not-allowed');
      $('#btn-convert').prop('disabled', false);
    });
  });
  
});

var utils = {
  makeId: function (length) {
    var result = '';
    var characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
    var charactersLength = characters.length;
    for (var i = 0; i < length; i++) {
      result += characters.charAt(Math.floor(Math.random() * charactersLength));
    }
    return result;
  },

  isYoutubeUrl: function (url) {
    var p = /^(?:https?:\/\/)?(?:www\.)?(?:m\.)?(?:youtu\.be\/|youtube\.com\/(?:embed\/|v\/|watch\?v=|watch\?.+&v=))((?:\w|-){11})(?:\S+)?$/;
    return url.match(p);
  },

  isMixcloudUrl: function (url) {
    var p = /^(?:https?:\/\/)?(?:www\.)?(?:m\.)?(?:mixcloud\.com\/)([a-zA-Z0-9-]+)\/([a-zA-Z0-9-]+)\/?$/;
    return url.match(p);
  },

  isSoundcloudUrl: function (url) {
    var p = /^(?:https?:\/\/)?(?:www\.)?(?:m\.)?(?:soundcloud\.com\/)([a-zA-Z0-9-]+)\/([a-zA-Z0-9-]+)\/?$/;
    return url.match(p);
  },

  isValidUrl: function (url) {
    if (!url) return false;
    if (this.isYoutubeUrl(url)
    || this.isMixcloudUrl(url)
    || this.isSoundcloudUrl(url)) return true;
    return false;
  }
}
