(function(window, undefined) {
  var dictionary = {
    "9b33f755-4bdd-412f-83c4-7a3131c45a47": "Login",
    "ba33203e-5448-4308-a12c-2222c818fbd1": "Show One",
    "30018489-9fa4-4fd9-9f7e-5617526f785f": "Registration",
    "4f650785-a768-43cc-8108-0e91a3f26cbd": "Edit",
    "4c1003a3-6b30-4b37-8c3f-03d48e6f9e67": "Welcome Page",
    "d12245cc-1680-458d-89dd-4f0d7fb22724": "Screen 1",
    "93fc5a8f-18e7-40ea-90ce-6da3f381620b": "New Listing",
    "f39803f7-df02-4169-93eb-7547fb8c961a": "Template 1",
    "bb8abf58-f55e-472d-af05-a7d1bb0cc014": "default"
  };

  var uriRE = /^(\/#)?(screens|templates|masters|scenarios)\/(.*)(\.html)?/;
  window.lookUpURL = function(fragment) {
    var matches = uriRE.exec(fragment || "") || [],
        folder = matches[2] || "",
        canvas = matches[3] || "",
        name, url;
    if(dictionary.hasOwnProperty(canvas)) { /* search by name */
      url = folder + "/" + canvas;
    }
    return url;
  };

  window.lookUpName = function(fragment) {
    var matches = uriRE.exec(fragment || "") || [],
        folder = matches[2] || "",
        canvas = matches[3] || "",
        name, canvasName;
    if(dictionary.hasOwnProperty(canvas)) { /* search by name */
      canvasName = dictionary[canvas];
    }
    return canvasName;
  };
})(window);