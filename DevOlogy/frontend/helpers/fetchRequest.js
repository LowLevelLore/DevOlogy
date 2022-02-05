import getCookie from "./getCookie";

const defaultHeaders = {
  Accept: "application/json",
  "X-Requested-With": "XMLHttpRequest", //Necessary to work with request.is_ajax()
  "X-CSRFToken": getCookie("csrftoken"),
};

const defaultCredentials = "same-origin";

/**
 * @param {string} path_ - Path to Fetch
 * @param {JSON} headers - Headers
 * @param {JSON} body - Body of the Request
 * @param {string} method - GET or POST
 * @param {string} credentials - include or same-origin
 * @param {function} next - Called after the request, with data as parameter.
 */
async function syncFetchRequest({
  path_,
  headers = defaultHeaders,
  body,
  method = "POST",
  credentials = defaultCredentials,
  next,
}) {
  await fetch(path_, {
    method: method,
    credentials: credentials,
    headers: headers,
    body: JSON.stringify(body),
  })
    .then((response) => response.json())
    .then((data) => {
      next(data);
    });
}

/**
 * @param {string} path_ - Path to Fetch
 * @param {JSON} headers - Headers
 * @param {JSON} body - Body of the Request
 * @param {string} method - GET or POST
 * @param {string} credentials - include or same-origin
 * @param {function} next - Called after the request, with data as parameter.
 */
async function fetchRequest({
  path_,
  headers = defaultHeaders,
  body,
  method = "POST",
  credentials = defaultCredentials,
  next,
}) {
  fetch(path_, {
    method: method,
    credentials: credentials,
    headers: headers,
    body: JSON.stringify(body),
  })
    .then((response) => response.json())
    .then((data) => {
      next(data);
    });
}

export { fetchRequest, syncFetchRequest };
