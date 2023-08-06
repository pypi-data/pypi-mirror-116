!function () {
    'use strict';

    var URL_PREFIX = '/cdn-cgi/l/email-protection#';
    var DIV_ELEM = document.createElement('div');

    function replaceAll(rootNode) {
        try {
            replaceEmailLinks(rootNode);
            replaceEmailTexts(rootNode);
            replaceInTemplates(rootNode);
        } catch (error) {
            showError(error);
        }
    }

    function replaceEmailLinks(rootNode) {
        var linkElems = rootNode.querySelectorAll('a');
        for (var i = 0; i < linkElems.length; ++i) try {
            var aElem = linkElems[i];
            var prefixIdx = aElem.href.indexOf(URL_PREFIX);
            if (prefixIdx > -1) {
                var startFrom = prefixIdx + URL_PREFIX.length;
                aElem.href = 'mailto:' + unmangleEmail(aElem.href, startFrom);
            };
        } catch (error) {
            showError(error);
        }
    }
    function replaceEmailTexts(rootNode) {
        var elemsToProcess = rootNode.querySelectorAll('.__cf_email__');
        for (var i = 0; i < elemsToProcess.length; ++i) try {
            var elem = elemsToProcess[i];
            var parentElem = elem.parentNode;
            var hexString = elem.getAttribute('data-cfemail');
            if (hexString) {
                var email = unmangleEmail(hexString, 0);
                var emailTextNode = document.createTextNode(email);
                parentElem.replaceChild(emailTextNode, elem);
            }
        } catch (error) {
            showError(error);
        }
    }
    function replaceInTemplates(rootNode) {
        var templateElems = rootNode.querySelectorAll('template');
        for (var i = 0; i < templateElems.length; ++i) try {
            replaceAll(templateElems[i].content);
        } catch (error) {
            showError(error);
        }
    }

    function unmangleEmail(hexString, startIdx) {
        var unmangled = '';
        var firstVal = parseHexVal(hexString, startIdx);
        for (var i = startIdx + 2; i < hexString.length; i += 2) {
            var charCode = parseHexVal(hexString, i) ^ firstVal;
            unmangled += String.fromCharCode(charCode);
        }
        try {
            var email = decodeURIComponent(escape(unmangled));
        } catch (error) {
            showError(error);
        }
        return getHrefValidValue(email);
    }
    function parseHexVal(hexString, idx) {
        var hexValue = hexString.substr(idx, 2);
        return parseInt(hexValue, 16);
    }
    function getHrefValidValue(url) {
        DIV_ELEM.innerHTML = '<a href="' + url.replace(/"/g, '&quot;') + '"></a>';
        return DIV_ELEM.childNodes[0].getAttribute('href') || '';
    }

    function showError(message) {
        try {
            if ('undefined' == typeof console) return;
            'error' in console ? console.error(message) : console.log(message);
        } catch (e) {
        }
    }

    function removeSelfFromScripts() {
        var self = document.currentScript || document.scripts[document.scripts.length - 1];
        self.parentNode.removeChild(self);
    }

    replaceAll(document);
    removeSelfFromScripts();
}();
