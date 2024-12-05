/**odoo-module **/

import { registry } from "@web/core/registry";
import { Component } from "@odoo/owl";

class MyCustomActions extends Components {}
MyCustomActions.template = "CustomActions"

registry.category("actions").add("custom_client_action",MyCustomActions);

// odoo.define('real_estate_ads.CustomAction',function(require){
//     "use strict";
//     var AbstractionAction = require('web.Abstraction');
//     var core = require('web.Core');

//     AbstractionAction.extend({
//         template: "",
//         start:function(){
//             console.log("Action")
//         }
//     })

//     core.action_registry.add("custom_client_action",CustomAction)
// });