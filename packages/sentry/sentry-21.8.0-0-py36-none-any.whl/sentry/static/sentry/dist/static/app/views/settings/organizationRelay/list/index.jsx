Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var orderBy_1 = tslib_1.__importDefault(require("lodash/orderBy"));
var activityList_1 = tslib_1.__importDefault(require("./activityList"));
var cardHeader_1 = tslib_1.__importDefault(require("./cardHeader"));
var utils_1 = require("./utils");
var waitingActivity_1 = tslib_1.__importDefault(require("./waitingActivity"));
var List = function (_a) {
    var relays = _a.relays, relayActivities = _a.relayActivities, onRefresh = _a.onRefresh, onDelete = _a.onDelete, onEdit = _a.onEdit, disabled = _a.disabled;
    var orderedRelays = orderBy_1.default(relays, function (relay) { return relay.created; }, ['desc']);
    var relaysByPublicKey = utils_1.getRelaysByPublicKey(orderedRelays, relayActivities);
    var renderCardContent = function (activities) {
        if (!activities.length) {
            return <waitingActivity_1.default onRefresh={onRefresh} disabled={disabled}/>;
        }
        return <activityList_1.default activities={activities}/>;
    };
    return (<div>
      {Object.keys(relaysByPublicKey).map(function (relayByPublicKey) {
            var _a = relaysByPublicKey[relayByPublicKey], name = _a.name, description = _a.description, created = _a.created, activities = _a.activities;
            return (<div key={relayByPublicKey}>
            <cardHeader_1.default publicKey={relayByPublicKey} name={name} description={description} created={created} onEdit={onEdit} onDelete={onDelete} disabled={disabled}/>
            {renderCardContent(activities)}
          </div>);
        })}
    </div>);
};
exports.default = List;
//# sourceMappingURL=index.jsx.map