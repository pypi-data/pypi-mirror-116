"use strict";
(self["webpackChunk_educational_technology_collective_etc_jupyterlab_nbgrader_validate"] = self["webpackChunk_educational_technology_collective_etc_jupyterlab_nbgrader_validate"] || []).push([["lib_index_js"],{

/***/ "./lib/handler.js":
/*!************************!*\
  !*** ./lib/handler.js ***!
  \************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "requestAPI": () => (/* binding */ requestAPI)
/* harmony export */ });
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/coreutils */ "webpack/sharing/consume/default/@jupyterlab/coreutils");
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/services */ "webpack/sharing/consume/default/@jupyterlab/services");
/* harmony import */ var _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__);


/**
 * Call the API extension
 *
 * @param endPoint API REST end point for the extension
 * @param init Initial values for the request
 * @returns The response body interpreted as JSON
 */
async function requestAPI(endPoint = '', init = {}) {
    // Make request to Jupyter API
    const settings = _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__.ServerConnection.makeSettings();
    const requestUrl = _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0__.URLExt.join(settings.baseUrl, 'jupyterlab-nbgrader-validate', // API Namespace
    endPoint);
    let response;
    try {
        response = await _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__.ServerConnection.makeRequest(requestUrl, init, settings);
    }
    catch (error) {
        throw new _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__.ServerConnection.NetworkError(error);
    }
    let data = await response.text();
    if (data.length > 0) {
        try {
            data = JSON.parse(data);
        }
        catch (error) {
            console.log('Not a JSON response body.', response);
        }
    }
    if (!response.ok) {
        throw new _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__.ServerConnection.ResponseError(response, data.message || data);
    }
    return data;
}


/***/ }),

/***/ "./lib/index.js":
/*!**********************!*\
  !*** ./lib/index.js ***!
  \**********************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "IValidateButtonExtension": () => (/* binding */ IValidateButtonExtension),
/* harmony export */   "ValidateButtonExtension": () => (/* binding */ ValidateButtonExtension),
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _lumino_disposable__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @lumino/disposable */ "webpack/sharing/consume/default/@lumino/disposable");
/* harmony import */ var _lumino_disposable__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_lumino_disposable__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @lumino/widgets */ "webpack/sharing/consume/default/@lumino/widgets");
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_lumino_widgets__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @lumino/coreutils */ "webpack/sharing/consume/default/@lumino/coreutils");
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_lumino_coreutils__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var _lumino_signaling__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @lumino/signaling */ "webpack/sharing/consume/default/@lumino/signaling");
/* harmony import */ var _lumino_signaling__WEBPACK_IMPORTED_MODULE_4___default = /*#__PURE__*/__webpack_require__.n(_lumino_signaling__WEBPACK_IMPORTED_MODULE_4__);
/* harmony import */ var _handler__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ./handler */ "./lib/handler.js");






const PLUGIN_ID = '@educational-technology-collective/etc_jupyterlab_nbgrader_validate:plugin';
const IValidateButtonExtension = new _lumino_coreutils__WEBPACK_IMPORTED_MODULE_3__.Token(PLUGIN_ID);
/**
 * Initialization data for the jupyterlab-nbgrader-validate extension.
 */
const plugin = {
    id: PLUGIN_ID,
    provides: IValidateButtonExtension,
    autoStart: true,
    activate
};
/**
 * A notebook widget extension that adds a button to the toolbar.
 */
class ValidateButtonExtension {
    constructor() {
        this._validateButtonClicked = new _lumino_signaling__WEBPACK_IMPORTED_MODULE_4__.Signal(this);
        this._validationResultsDisplayed = new _lumino_signaling__WEBPACK_IMPORTED_MODULE_4__.Signal(this);
        this._validationResultsDismissed = new _lumino_signaling__WEBPACK_IMPORTED_MODULE_4__.Signal(this);
    }
    /**
     * Create a new extension for the notebook panel widget.
     */
    createNew(panel, context) {
        const validate = async () => {
            try {
                this._validateButtonClicked.emit({
                    event_name: 'validate_button_clicked',
                    notebook_panel: panel
                });
                //  Emit a Signal when the validate button is clicked; 
                //  hence, emit a Signal at the start of the handler.
                let validateButton = document.getElementsByClassName('validate-button')[0];
                validateButton.children[0].children[0].innerHTML = "Validating...";
                // POST request
                const notebookPath = panel.context.path;
                const dataToSend = { name: notebookPath };
                let reply;
                try {
                    reply = await (0,_handler__WEBPACK_IMPORTED_MODULE_5__.requestAPI)('validate', {
                        body: JSON.stringify(dataToSend),
                        method: 'POST'
                    });
                    console.log(reply);
                }
                catch (reason) {
                    throw new Error(`Error on POST /jupyterlab-nbgrader-validate/validate ${dataToSend}.\n${reason}`);
                }
                finally {
                    validateButton.children[0].children[0].innerHTML = "Validate";
                }
                let body = document.createElement('div');
                let pre = document.createElement('pre');
                pre.innerText = reply.output;
                body.appendChild(pre);
                this._validationResultsDisplayed.emit({
                    event_name: 'validate_results_displayed',
                    notebook_panel: panel,
                    message: reply.output
                });
                //  Emit a Signal when the Validation Results are displayed; 
                //  hence, emit a Signal just prior to displaying the results.
                let result = await (0,_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_2__.showDialog)({
                    title: 'Validation Results',
                    body: new _lumino_widgets__WEBPACK_IMPORTED_MODULE_1__.Widget({ node: body }),
                    buttons: [_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_2__.Dialog.okButton()],
                });
                this._validationResultsDismissed.emit({
                    event_name: 'validate_results_dismissed',
                    notebook_panel: panel,
                    message: result
                });
                //  Emit a Signal once the dialog has been dismissed (either accepted or declined);
                //  hence, emit a Signal with the result message.
            }
            catch (e) {
                console.error(e);
            }
        };
        const validateButton = new _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_2__.ToolbarButton({
            className: 'validate-button',
            label: 'Validate',
            onClick: validate,
            tooltip: 'Validate'
        });
        panel.toolbar.insertItem(10, 'validateNotebook', validateButton);
        return new _lumino_disposable__WEBPACK_IMPORTED_MODULE_0__.DisposableDelegate(() => {
            validateButton.dispose();
        });
    }
    get validateButtonClicked() {
        return this._validateButtonClicked;
    }
    get validationResultsDisplayed() {
        return this._validationResultsDisplayed;
    }
    get validationResultsDismissed() {
        return this._validationResultsDismissed;
    }
}
/**
 * Activate the extension.
 */
function activate(app) {
    const validateButtonExtension = new ValidateButtonExtension();
    app.docRegistry.addWidgetExtension('Notebook', validateButtonExtension);
    return validateButtonExtension;
}
/**
 * Export the plugin as default.
 */
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (plugin);


/***/ })

}]);
//# sourceMappingURL=lib_index_js.a5539fce421bb5f21cc3.js.map