// Copyright (c) Afshin T. Darian
// Distributed under the terms of the Modified BSD License.

import {
  DOMWidgetModel,
  DOMWidgetView,
  ISerializers,
} from '@jupyter-widgets/base';

import { MODULE_NAME, MODULE_VERSION } from './version';

// Import the CSS
import '../css/widget.css';

export class LifeModel extends DOMWidgetModel {
  defaults(): any {
    return {
      ...super.defaults(),
      _model_name: LifeModel.model_name,
      _model_module: LifeModel.model_module,
      _model_module_version: LifeModel.model_module_version,
      _view_name: LifeModel.view_name,
      _view_module: LifeModel.view_module,
      _view_module_version: LifeModel.view_module_version,
      value: 'Hello World',
    };
  }

  static serializers: ISerializers = {
    ...DOMWidgetModel.serializers,
    // Add any extra serializers here
  };

  static model_name = 'LifeModel';
  static model_module = MODULE_NAME;
  static model_module_version = MODULE_VERSION;
  static view_name = 'LifeView';
  static view_module = MODULE_NAME;
  static view_module_version = MODULE_VERSION;
}

export class LifeView extends DOMWidgetView {
  render(): any {
    this.el.classList.add('ipylife');

    this.value_changed();
    this.model.on('change:value', this.value_changed, this);
  }

  value_changed(): void {
    this.el.textContent = this.model.get('value');
  }
}
