"use strict";
(self["webpackChunk_educational_technology_collective_etc_jupyterlab_telemetry_coursera"] = self["webpackChunk_educational_technology_collective_etc_jupyterlab_telemetry_coursera"] || []).push([["lib_index_js"],{

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
    const requestUrl = _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0__.URLExt.join(settings.baseUrl, 'etc-jupyterlab-telemetry-coursera', // API Namespace
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
/* harmony export */   "AWSAPIGatewayAdapter": () => (/* binding */ AWSAPIGatewayAdapter),
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/notebook */ "webpack/sharing/consume/default/@jupyterlab/notebook");
/* harmony import */ var _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _educational_technology_collective_etc_jupyterlab_telemetry_extension__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @educational-technology-collective/etc_jupyterlab_telemetry_extension */ "webpack/sharing/consume/default/@educational-technology-collective/etc_jupyterlab_telemetry_extension");
/* harmony import */ var _educational_technology_collective_etc_jupyterlab_telemetry_extension__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_educational_technology_collective_etc_jupyterlab_telemetry_extension__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _educational_technology_collective_etc_jupyterlab_telemetry_validate_button__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @educational-technology-collective/etc_jupyterlab_telemetry_validate_button */ "webpack/sharing/consume/default/@educational-technology-collective/etc_jupyterlab_telemetry_validate_button");
/* harmony import */ var _educational_technology_collective_etc_jupyterlab_telemetry_validate_button__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_educational_technology_collective_etc_jupyterlab_telemetry_validate_button__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _educational_technology_collective_etc_jupyterlab_nbgrader_validate__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @educational-technology-collective/etc_jupyterlab_nbgrader_validate */ "webpack/sharing/consume/default/@educational-technology-collective/etc_jupyterlab_nbgrader_validate");
/* harmony import */ var _educational_technology_collective_etc_jupyterlab_nbgrader_validate__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_educational_technology_collective_etc_jupyterlab_nbgrader_validate__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var _handler__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ./handler */ "./lib/handler.js");
/* harmony import */ var _educational_technology_collective_etc_jupyterlab_notebook_state__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @educational-technology-collective/etc_jupyterlab_notebook_state */ "webpack/sharing/consume/default/@educational-technology-collective/etc_jupyterlab_notebook_state");
/* harmony import */ var _educational_technology_collective_etc_jupyterlab_notebook_state__WEBPACK_IMPORTED_MODULE_4___default = /*#__PURE__*/__webpack_require__.n(_educational_technology_collective_etc_jupyterlab_notebook_state__WEBPACK_IMPORTED_MODULE_4__);






const PLUGIN_ID = '@educational-technology-collective/etc_jupyterlab_telemetry_coursera:plugin';
class AWSAPIGatewayAdapter {
    constructor() {
        this._userId = (async () => {
            try { // to get the user id.
                return await (0,_handler__WEBPACK_IMPORTED_MODULE_5__.requestAPI)("id");
            }
            catch (e) {
                console.error(`Error on GET id.\n${e}`);
                return "UNDEFINED";
            }
            //  This request is specific to the Coursera environment; hence, it may not be relevant in other contexts.
            //  The request for the `id` resource will return the value of the WORKSPACE_ID environment variable that is assigned on the server.
        })();
    }
    adaptMessage(sender, data) {
        (async () => {
            try {
                //
                data = Object.assign(Object.assign({}, data), {
                    user_id: await this._userId
                });
                //  The user id is not a characteristic of the event; hence, it is added late. 
                console.log(data);
                let response = await (0,_handler__WEBPACK_IMPORTED_MODULE_5__.requestAPI)("s3", { method: "POST", body: JSON.stringify(data) });
                //console.log(response);
            }
            catch (e) {
                console.error(e);
            }
        })();
    }
}
/**
 * Initialization data for the @educational-technology-collective/etc_jupyterlab_telemetry_coursera extension.
 */
const plugin = {
    id: PLUGIN_ID,
    autoStart: true,
    requires: [
        _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_0__.INotebookTracker,
        _educational_technology_collective_etc_jupyterlab_telemetry_extension__WEBPACK_IMPORTED_MODULE_1__.IETCJupyterLabTelemetryLibraryConstructor,
        _educational_technology_collective_etc_jupyterlab_telemetry_validate_button__WEBPACK_IMPORTED_MODULE_2__.IETCJupyterLabTelemetryValidateButtonConstructor,
        _educational_technology_collective_etc_jupyterlab_nbgrader_validate__WEBPACK_IMPORTED_MODULE_3__.IValidateButtonExtension,
        _educational_technology_collective_etc_jupyterlab_notebook_state__WEBPACK_IMPORTED_MODULE_4__.IETCJupyterLabNotebookState
    ],
    activate: (app, notebookTracker, ETCJupyterLabTelemetryLibrary, ETCJupyterLabTelemetryValidateButton, validateButtonExtension, NotebookState) => {
        console.log('JupyterLab extension @educational-technology-collective/etc_jupyterlab_telemetry_coursera is activated!');
        let messageAdapter = new AWSAPIGatewayAdapter();
        notebookTracker.widgetAdded.connect(async (sender, notebookPanel) => {
            await notebookPanel.revealed;
            await notebookPanel.sessionContext.ready;
            let notebookState = new NotebookState({ notebookPanel });
            let etcJupyterLabTelemetryLibrary = new ETCJupyterLabTelemetryLibrary({
                notebookPanel,
                notebookState
            });
            etcJupyterLabTelemetryLibrary.notebookOpenEvent.notebookOpened.connect(messageAdapter.adaptMessage, messageAdapter);
            etcJupyterLabTelemetryLibrary.notebookSaveEvent.notebookSaved.connect(messageAdapter.adaptMessage, messageAdapter);
            etcJupyterLabTelemetryLibrary.activeCellChangeEvent.activeCellChanged.connect(messageAdapter.adaptMessage, messageAdapter);
            etcJupyterLabTelemetryLibrary.cellAddEvent.cellAdded.connect(messageAdapter.adaptMessage, messageAdapter);
            etcJupyterLabTelemetryLibrary.cellRemoveEvent.cellRemoved.connect(messageAdapter.adaptMessage, messageAdapter);
            etcJupyterLabTelemetryLibrary.notebookScrollEvent.notebookScrolled.connect(messageAdapter.adaptMessage, messageAdapter);
            etcJupyterLabTelemetryLibrary.cellExecutionEvent.cellExecuted.connect(messageAdapter.adaptMessage, messageAdapter);
            etcJupyterLabTelemetryLibrary.cellErrorEvent.cellErrored.connect(messageAdapter.adaptMessage, messageAdapter);
            let etcJupyterLabTelemetryValidateButton = new ETCJupyterLabTelemetryValidateButton({
                notebookPanel,
                validateButtonExtension,
                notebookState
            });
            etcJupyterLabTelemetryValidateButton.validateButtonClicked.connect(messageAdapter.adaptMessage, messageAdapter);
            etcJupyterLabTelemetryValidateButton.validationResultsDisplayed.connect(messageAdapter.adaptMessage, messageAdapter);
            etcJupyterLabTelemetryValidateButton.validationResultsDismissed.connect(messageAdapter.adaptMessage, messageAdapter);
        });
    }
};
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (plugin);


/***/ })

}]);
//# sourceMappingURL=lib_index_js.0cf2271c47ea3b289924.js.map