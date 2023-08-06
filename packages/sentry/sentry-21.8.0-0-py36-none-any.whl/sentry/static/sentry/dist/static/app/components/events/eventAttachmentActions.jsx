Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_1 = require("react");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var button_1 = tslib_1.__importDefault(require("app/components/button"));
var buttonBar_1 = tslib_1.__importDefault(require("app/components/buttonBar"));
var confirm_1 = tslib_1.__importDefault(require("app/components/confirm"));
var icons_1 = require("app/icons");
var locale_1 = require("app/locale");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var withApi_1 = tslib_1.__importDefault(require("app/utils/withApi"));
var EventAttachmentActions = /** @class */ (function (_super) {
    tslib_1.__extends(EventAttachmentActions, _super);
    function EventAttachmentActions() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    EventAttachmentActions.prototype.handlePreview = function () {
        var _a = this.props, onPreview = _a.onPreview, attachmentId = _a.attachmentId;
        if (onPreview) {
            onPreview(attachmentId);
        }
    };
    EventAttachmentActions.prototype.render = function () {
        var _this = this;
        var _a = this.props, url = _a.url, withPreviewButton = _a.withPreviewButton, hasPreview = _a.hasPreview, previewIsOpen = _a.previewIsOpen, onDelete = _a.onDelete, attachmentId = _a.attachmentId;
        return (<buttonBar_1.default gap={1}>
        <confirm_1.default confirmText={locale_1.t('Delete')} message={locale_1.t('Are you sure you wish to delete this file?')} priority="danger" onConfirm={function () { return onDelete(attachmentId); }} disabled={!url}>
          <button_1.default size="xsmall" icon={<icons_1.IconDelete size="xs"/>} label={locale_1.t('Delete')} disabled={!url} title={!url ? locale_1.t('Insufficient permissions to delete attachments') : undefined}/>
        </confirm_1.default>

        <DownloadButton size="xsmall" icon={<icons_1.IconDownload size="xs"/>} href={url ? url + "?download=1" : ''} disabled={!url} title={!url ? locale_1.t('Insufficient permissions to download attachments') : undefined} label={locale_1.t('Download')}/>

        {withPreviewButton && (<DownloadButton size="xsmall" disabled={!url || !hasPreview} priority={previewIsOpen ? 'primary' : 'default'} icon={<icons_1.IconShow size="xs"/>} onClick={function () { return _this.handlePreview(); }} title={!url
                    ? locale_1.t('Insufficient permissions to preview attachments')
                    : !hasPreview
                        ? locale_1.t('This attachment cannot be previewed')
                        : undefined}>
            {locale_1.t('Preview')}
          </DownloadButton>)}
      </buttonBar_1.default>);
    };
    return EventAttachmentActions;
}(react_1.Component));
var DownloadButton = styled_1.default(button_1.default)(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  margin-right: ", ";\n"], ["\n  margin-right: ", ";\n"])), space_1.default(0.5));
exports.default = withApi_1.default(EventAttachmentActions);
var templateObject_1;
//# sourceMappingURL=eventAttachmentActions.jsx.map