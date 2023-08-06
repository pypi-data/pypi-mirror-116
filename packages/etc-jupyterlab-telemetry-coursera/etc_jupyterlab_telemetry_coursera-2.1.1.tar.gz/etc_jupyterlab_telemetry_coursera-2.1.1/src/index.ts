import {
  JupyterFrontEnd,
  JupyterFrontEndPlugin
} from '@jupyterlab/application';

import { INotebookTracker, NotebookPanel } from '@jupyterlab/notebook';

import {
  IETCJupyterLabTelemetryLibraryConstructor
} from "@educational-technology-collective/etc_jupyterlab_telemetry_extension";


import { IETCJupyterLabTelemetryValidateButtonConstructor } from "@educational-technology-collective/etc_jupyterlab_telemetry_validate_button";

import { IValidateButtonExtension } from "@educational-technology-collective/etc_jupyterlab_nbgrader_validate";

import { requestAPI } from './handler';

import {
  IETCJupyterLabNotebookState as INotebookState
} from "@educational-technology-collective/etc_jupyterlab_notebook_state";

const PLUGIN_ID = '@educational-technology-collective/etc_jupyterlab_telemetry_coursera:plugin';

export class AWSAPIGatewayAdapter {

  private _userId: Promise<string>;

  constructor() {

    this._userId = (async () => {

      try { // to get the user id.
        return await requestAPI<string>("id");
      } catch (e) {
        console.error(`Error on GET id.\n${e}`);
        return "UNDEFINED";
      }
      //  This request is specific to the Coursera environment; hence, it may not be relevant in other contexts.
      //  The request for the `id` resource will return the value of the WORKSPACE_ID environment variable that is assigned on the server.
    })();
  }

  adaptMessage(
    sender: any,
    data: object
  ): void {

    (async () => {
      try {

        //
        data = {
          ...data,
          ...{
            user_id: await this._userId
          }
        }
        //  The user id is not a characteristic of the event; hence, it is added late. 

        console.log(data);

        let response = await requestAPI<string>("s3", { method: "POST", body: JSON.stringify(data) });

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
const plugin: JupyterFrontEndPlugin<void> = {
  id: PLUGIN_ID,
  autoStart: true,
  requires: [
    INotebookTracker,
    IETCJupyterLabTelemetryLibraryConstructor,
    IETCJupyterLabTelemetryValidateButtonConstructor,
    IValidateButtonExtension,
    INotebookState
  ],
  activate: (
    app: JupyterFrontEnd,
    notebookTracker: INotebookTracker,
    ETCJupyterLabTelemetryLibrary: IETCJupyterLabTelemetryLibraryConstructor,
    ETCJupyterLabTelemetryValidateButton: IETCJupyterLabTelemetryValidateButtonConstructor,
    validateButtonExtension: IValidateButtonExtension,
    NotebookState: INotebookState
  ) => {
    console.log('JupyterLab extension @educational-technology-collective/etc_jupyterlab_telemetry_coursera is activated!');

    let messageAdapter = new AWSAPIGatewayAdapter();

    notebookTracker.widgetAdded.connect(async (sender: INotebookTracker, notebookPanel: NotebookPanel) => {

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

export default plugin;
