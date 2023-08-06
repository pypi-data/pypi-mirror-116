Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var imageViewer_1 = tslib_1.__importDefault(require("app/components/events/attachmentViewers/imageViewer"));
var jsonViewer_1 = tslib_1.__importDefault(require("app/components/events/attachmentViewers/jsonViewer"));
var logFileViewer_1 = tslib_1.__importDefault(require("app/components/events/attachmentViewers/logFileViewer"));
var rrwebJsonViewer_1 = tslib_1.__importDefault(require("app/components/events/attachmentViewers/rrwebJsonViewer"));
var eventAttachmentActions_1 = tslib_1.__importDefault(require("app/components/events/eventAttachmentActions"));
var eventDataSection_1 = tslib_1.__importDefault(require("app/components/events/eventDataSection"));
var fileSize_1 = tslib_1.__importDefault(require("app/components/fileSize"));
var panels_1 = require("app/components/panels");
var locale_1 = require("app/locale");
var overflowEllipsis_1 = tslib_1.__importDefault(require("app/styles/overflowEllipsis"));
var attachmentUrl_1 = tslib_1.__importDefault(require("app/utils/attachmentUrl"));
var withApi_1 = tslib_1.__importDefault(require("app/utils/withApi"));
var eventAttachmentsCrashReportsNotice_1 = tslib_1.__importDefault(require("./eventAttachmentsCrashReportsNotice"));
var EventAttachments = /** @class */ (function (_super) {
    tslib_1.__extends(EventAttachments, _super);
    function EventAttachments() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            expanded: false,
            attachmentPreviews: {},
        };
        _this.attachmentPreviewIsOpen = function (attachment) {
            return !!_this.state.attachmentPreviews[attachment.id];
        };
        return _this;
    }
    EventAttachments.prototype.getInlineAttachmentRenderer = function (attachment) {
        switch (attachment.mimetype) {
            case 'text/plain':
                return attachment.size > 0 ? logFileViewer_1.default : undefined;
            case 'text/json':
            case 'text/x-json':
            case 'application/json':
                if (attachment.name === 'rrweb.json') {
                    return rrwebJsonViewer_1.default;
                }
                return jsonViewer_1.default;
            case 'image/jpeg':
            case 'image/png':
            case 'image/gif':
                return imageViewer_1.default;
            default:
                return undefined;
        }
    };
    EventAttachments.prototype.hasInlineAttachmentRenderer = function (attachment) {
        return !!this.getInlineAttachmentRenderer(attachment);
    };
    EventAttachments.prototype.renderInlineAttachment = function (attachment) {
        var Component = this.getInlineAttachmentRenderer(attachment);
        if (!Component || !this.attachmentPreviewIsOpen(attachment)) {
            return null;
        }
        return (<AttachmentPreviewWrapper>
        <Component orgId={this.props.orgId} projectId={this.props.projectId} event={this.props.event} attachment={attachment}/>
      </AttachmentPreviewWrapper>);
    };
    EventAttachments.prototype.togglePreview = function (attachment) {
        this.setState(function (_a) {
            var _b;
            var attachmentPreviews = _a.attachmentPreviews;
            return ({
                attachmentPreviews: tslib_1.__assign(tslib_1.__assign({}, attachmentPreviews), (_b = {}, _b[attachment.id] = !attachmentPreviews[attachment.id], _b)),
            });
        });
    };
    EventAttachments.prototype.render = function () {
        var _this = this;
        var _a = this.props, event = _a.event, projectId = _a.projectId, orgId = _a.orgId, location = _a.location, attachments = _a.attachments, onDeleteAttachment = _a.onDeleteAttachment;
        var crashFileStripped = event.metadata.stripped_crash;
        if (!attachments.length && !crashFileStripped) {
            return null;
        }
        var title = locale_1.t('Attachments (%s)', attachments.length);
        var lastAttachmentPreviewed = attachments.length > 0 &&
            this.attachmentPreviewIsOpen(attachments[attachments.length - 1]);
        return (<eventDataSection_1.default type="attachments" title={title}>
        {crashFileStripped && (<eventAttachmentsCrashReportsNotice_1.default orgSlug={orgId} projectSlug={projectId} groupId={event.groupID} location={location}/>)}

        {attachments.length > 0 && (<StyledPanelTable headers={[
                    <Name key="name">{locale_1.t('File Name')}</Name>,
                    <Size key="size">{locale_1.t('Size')}</Size>,
                    locale_1.t('Actions'),
                ]}>
            {attachments.map(function (attachment) { return (<React.Fragment key={attachment.id}>
                <Name>{attachment.name}</Name>
                <Size>
                  <fileSize_1.default bytes={attachment.size}/>
                </Size>
                <attachmentUrl_1.default projectId={projectId} eventId={event.id} attachment={attachment}>
                  {function (url) { return (<div>
                      <eventAttachmentActions_1.default url={url} onDelete={onDeleteAttachment} onPreview={function (_attachmentId) { return _this.togglePreview(attachment); }} withPreviewButton previewIsOpen={_this.attachmentPreviewIsOpen(attachment)} hasPreview={_this.hasInlineAttachmentRenderer(attachment)} attachmentId={attachment.id}/>
                    </div>); }}
                </attachmentUrl_1.default>
                {_this.renderInlineAttachment(attachment)}
                {/* XXX: hack to deal with table grid borders */}
                {lastAttachmentPreviewed && (<React.Fragment>
                    <div style={{ display: 'none' }}/>
                    <div style={{ display: 'none' }}/>
                  </React.Fragment>)}
              </React.Fragment>); })}
          </StyledPanelTable>)}
      </eventDataSection_1.default>);
    };
    return EventAttachments;
}(React.Component));
exports.default = withApi_1.default(EventAttachments);
var StyledPanelTable = styled_1.default(panels_1.PanelTable)(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  grid-template-columns: 1fr auto auto;\n"], ["\n  grid-template-columns: 1fr auto auto;\n"])));
var Name = styled_1.default('div')(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  ", ";\n"], ["\n  ", ";\n"])), overflowEllipsis_1.default);
var Size = styled_1.default('div')(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  text-align: right;\n"], ["\n  text-align: right;\n"])));
var AttachmentPreviewWrapper = styled_1.default('div')(templateObject_4 || (templateObject_4 = tslib_1.__makeTemplateObject(["\n  grid-column: auto / span 3;\n  border: none;\n  padding: 0;\n"], ["\n  grid-column: auto / span 3;\n  border: none;\n  padding: 0;\n"])));
var templateObject_1, templateObject_2, templateObject_3, templateObject_4;
//# sourceMappingURL=eventAttachments.jsx.map