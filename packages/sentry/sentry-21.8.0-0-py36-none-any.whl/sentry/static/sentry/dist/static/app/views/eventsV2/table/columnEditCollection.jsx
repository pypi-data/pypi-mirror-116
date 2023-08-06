Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var react_dom_1 = tslib_1.__importDefault(require("react-dom"));
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var feature_1 = tslib_1.__importDefault(require("app/components/acl/feature"));
var parser_1 = require("app/components/arithmeticInput/parser");
var button_1 = tslib_1.__importDefault(require("app/components/button"));
var styles_1 = require("app/components/charts/styles");
var featureBadge_1 = tslib_1.__importDefault(require("app/components/featureBadge"));
var icons_1 = require("app/icons");
var locale_1 = require("app/locale");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var analytics_1 = require("app/utils/analytics");
var fields_1 = require("app/utils/discover/fields");
var theme_1 = tslib_1.__importDefault(require("app/utils/theme"));
var touch_1 = require("app/utils/touch");
var userselect_1 = require("app/utils/userselect");
var queryField_1 = require("./queryField");
var types_1 = require("./types");
var DRAG_CLASS = 'draggable-item';
var GHOST_PADDING = 4;
var MAX_COL_COUNT = 20;
var PlaceholderPosition;
(function (PlaceholderPosition) {
    PlaceholderPosition[PlaceholderPosition["TOP"] = 0] = "TOP";
    PlaceholderPosition[PlaceholderPosition["BOTTOM"] = 1] = "BOTTOM";
})(PlaceholderPosition || (PlaceholderPosition = {}));
var ColumnEditCollection = /** @class */ (function (_super) {
    tslib_1.__extends(ColumnEditCollection, _super);
    function ColumnEditCollection() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            isDragging: false,
            draggingIndex: void 0,
            draggingTargetIndex: void 0,
            draggingGrabbedOffset: void 0,
            error: new Map(),
            left: void 0,
            top: void 0,
        };
        _this.previousUserSelect = null;
        _this.portal = null;
        _this.dragGhostRef = React.createRef();
        // Signal to the parent that a new column has been added.
        _this.handleAddColumn = function () {
            var newColumn = { kind: 'field', field: '' };
            _this.props.onChange(tslib_1.__spreadArray(tslib_1.__spreadArray([], tslib_1.__read(_this.props.columns)), [newColumn]));
        };
        _this.handleAddEquation = function () {
            var organization = _this.props.organization;
            var newColumn = { kind: types_1.FieldValueKind.EQUATION, field: '' };
            analytics_1.trackAnalyticsEvent({
                eventKey: 'discover_v2.add_equation',
                eventName: 'Discoverv2: Equation added',
                organization_id: parseInt(organization.id, 10),
            });
            _this.props.onChange(tslib_1.__spreadArray(tslib_1.__spreadArray([], tslib_1.__read(_this.props.columns)), [newColumn]));
        };
        _this.handleUpdateColumn = function (index, updatedColumn) {
            var newColumns = tslib_1.__spreadArray([], tslib_1.__read(_this.props.columns));
            if (updatedColumn.kind === 'equation') {
                _this.setState(function (prevState) {
                    var error = new Map(prevState.error);
                    error.set(index, parser_1.parseArithmetic(updatedColumn.field).error);
                    return tslib_1.__assign(tslib_1.__assign({}, prevState), { error: error });
                });
            }
            else {
                // Update any equations that contain the existing column
                _this.updateEquationFields(newColumns, index, updatedColumn);
            }
            newColumns.splice(index, 1, updatedColumn);
            _this.props.onChange(newColumns);
        };
        _this.updateEquationFields = function (newColumns, index, updatedColumn) {
            var e_1, _a;
            var oldColumn = newColumns[index];
            var existingColumn = fields_1.generateFieldAsString(newColumns[index]);
            var updatedColumnString = fields_1.generateFieldAsString(updatedColumn);
            if (!fields_1.isLegalEquationColumn(updatedColumn) || fields_1.hasDuplicate(newColumns, oldColumn)) {
                return;
            }
            // Find the equations in the list of columns
            for (var i = 0; i < newColumns.length; i++) {
                var newColumn = newColumns[i];
                if (newColumn.kind === 'equation') {
                    var result = parser_1.parseArithmetic(newColumn.field);
                    var newEquation = '';
                    // Track where to continue from, not reconstructing from result so we don't have to worry
                    // about spacing
                    var lastIndex = 0;
                    // the parser separates fields & functions, so we only need to check one
                    var fields = oldColumn.kind === 'function' ? result.tc.functions : result.tc.fields;
                    try {
                        // for each field, add the text before it, then the new function and update index
                        // to be where we want to start again
                        for (var fields_2 = (e_1 = void 0, tslib_1.__values(fields)), fields_2_1 = fields_2.next(); !fields_2_1.done; fields_2_1 = fields_2.next()) {
                            var field = fields_2_1.value;
                            if (field.term === existingColumn && lastIndex !== field.location.end.offset) {
                                newEquation +=
                                    newColumn.field.substring(lastIndex, field.location.start.offset) +
                                        updatedColumnString;
                                lastIndex = field.location.end.offset;
                            }
                        }
                    }
                    catch (e_1_1) { e_1 = { error: e_1_1 }; }
                    finally {
                        try {
                            if (fields_2_1 && !fields_2_1.done && (_a = fields_2.return)) _a.call(fields_2);
                        }
                        finally { if (e_1) throw e_1.error; }
                    }
                    // Add whatever remains to be added from the equation, if existing field wasn't found
                    // add the entire equation
                    newEquation += newColumn.field.substring(lastIndex);
                    newColumns[i] = {
                        kind: 'equation',
                        field: newEquation,
                    };
                }
            }
        };
        _this.onDragMove = function (event) {
            var _a, _b;
            var _c = _this.state, isDragging = _c.isDragging, draggingTargetIndex = _c.draggingTargetIndex, draggingGrabbedOffset = _c.draggingGrabbedOffset;
            if (!isDragging || !['mousemove', 'touchmove'].includes(event.type)) {
                return;
            }
            event.preventDefault();
            event.stopPropagation();
            var pointerX = touch_1.getPointerPosition(event, 'pageX');
            var pointerY = touch_1.getPointerPosition(event, 'pageY');
            var dragOffsetX = (_a = draggingGrabbedOffset === null || draggingGrabbedOffset === void 0 ? void 0 : draggingGrabbedOffset.x) !== null && _a !== void 0 ? _a : 0;
            var dragOffsetY = (_b = draggingGrabbedOffset === null || draggingGrabbedOffset === void 0 ? void 0 : draggingGrabbedOffset.y) !== null && _b !== void 0 ? _b : 0;
            if (_this.dragGhostRef.current) {
                // move the ghost box
                var ghostDOM = _this.dragGhostRef.current;
                // Adjust so cursor is over the grab handle.
                ghostDOM.style.left = pointerX - dragOffsetX + "px";
                ghostDOM.style.top = pointerY - dragOffsetY + "px";
            }
            var dragItems = document.querySelectorAll("." + DRAG_CLASS);
            // Find the item that the ghost is currently over.
            var targetIndex = Array.from(dragItems).findIndex(function (dragItem) {
                var rects = dragItem.getBoundingClientRect();
                var top = pointerY;
                var thresholdStart = window.scrollY + rects.top;
                var thresholdEnd = window.scrollY + rects.top + rects.height;
                return top >= thresholdStart && top <= thresholdEnd;
            });
            if (targetIndex >= 0 && targetIndex !== draggingTargetIndex) {
                _this.setState({ draggingTargetIndex: targetIndex });
            }
        };
        _this.onDragEnd = function (event) {
            if (!_this.state.isDragging || !['mouseup', 'touchend'].includes(event.type)) {
                return;
            }
            var sourceIndex = _this.state.draggingIndex;
            var targetIndex = _this.state.draggingTargetIndex;
            if (typeof sourceIndex !== 'number' || typeof targetIndex !== 'number') {
                return;
            }
            // remove listeners that were attached in startColumnDrag
            _this.cleanUpListeners();
            // restore body user-select values
            if (_this.previousUserSelect) {
                userselect_1.setBodyUserSelect(_this.previousUserSelect);
                _this.previousUserSelect = null;
            }
            // Reorder columns and trigger change.
            var newColumns = tslib_1.__spreadArray([], tslib_1.__read(_this.props.columns));
            var removed = newColumns.splice(sourceIndex, 1);
            newColumns.splice(targetIndex, 0, removed[0]);
            _this.checkColumnErrors(newColumns);
            _this.props.onChange(newColumns);
            _this.setState({
                isDragging: false,
                left: undefined,
                top: undefined,
                draggingIndex: undefined,
                draggingTargetIndex: undefined,
                draggingGrabbedOffset: undefined,
            });
        };
        return _this;
    }
    ColumnEditCollection.prototype.componentDidMount = function () {
        if (!this.portal) {
            var portal = document.createElement('div');
            portal.style.position = 'absolute';
            portal.style.top = '0';
            portal.style.left = '0';
            portal.style.zIndex = String(theme_1.default.zIndex.modal);
            this.portal = portal;
            document.body.appendChild(this.portal);
        }
        this.checkColumnErrors(this.props.columns);
    };
    ColumnEditCollection.prototype.componentWillUnmount = function () {
        if (this.portal) {
            document.body.removeChild(this.portal);
        }
        this.cleanUpListeners();
    };
    ColumnEditCollection.prototype.checkColumnErrors = function (columns) {
        var error = new Map();
        for (var i = 0; i < columns.length; i += 1) {
            var column = columns[i];
            if (column.kind === 'equation') {
                var result = parser_1.parseArithmetic(column.field);
                if (result.error) {
                    error.set(i, result.error);
                }
            }
        }
        this.setState({ error: error });
    };
    ColumnEditCollection.prototype.keyForColumn = function (column, isGhost) {
        if (column.kind === 'function') {
            return tslib_1.__spreadArray(tslib_1.__spreadArray([], tslib_1.__read(column.function)), [isGhost]).join(':');
        }
        return tslib_1.__spreadArray(tslib_1.__spreadArray([], tslib_1.__read(column.field)), [isGhost]).join(':');
    };
    ColumnEditCollection.prototype.cleanUpListeners = function () {
        if (this.state.isDragging) {
            window.removeEventListener('mousemove', this.onDragMove);
            window.removeEventListener('touchmove', this.onDragMove);
            window.removeEventListener('mouseup', this.onDragEnd);
            window.removeEventListener('touchend', this.onDragEnd);
        }
    };
    ColumnEditCollection.prototype.removeColumn = function (index) {
        var newColumns = tslib_1.__spreadArray([], tslib_1.__read(this.props.columns));
        newColumns.splice(index, 1);
        this.checkColumnErrors(newColumns);
        this.props.onChange(newColumns);
    };
    ColumnEditCollection.prototype.startDrag = function (event, index) {
        var isDragging = this.state.isDragging;
        if (isDragging || !['mousedown', 'touchstart'].includes(event.type)) {
            return;
        }
        event.preventDefault();
        event.stopPropagation();
        var top = touch_1.getPointerPosition(event, 'pageY');
        var left = touch_1.getPointerPosition(event, 'pageX');
        // Compute where the user clicked on the drag handle. Avoids the element
        // jumping from the cursor on mousedown.
        var _a = Array.from(document.querySelectorAll("." + DRAG_CLASS))
            .find(function (n) { return n.contains(event.currentTarget); })
            .getBoundingClientRect(), x = _a.x, y = _a.y;
        var draggingGrabbedOffset = {
            x: left - x + GHOST_PADDING,
            y: top - y + GHOST_PADDING,
        };
        // prevent the user from selecting things when dragging a column.
        this.previousUserSelect = userselect_1.setBodyUserSelect({
            userSelect: 'none',
            MozUserSelect: 'none',
            msUserSelect: 'none',
            webkitUserSelect: 'none',
        });
        // attach event listeners so that the mouse cursor can drag anywhere
        window.addEventListener('mousemove', this.onDragMove);
        window.addEventListener('touchmove', this.onDragMove);
        window.addEventListener('mouseup', this.onDragEnd);
        window.addEventListener('touchend', this.onDragEnd);
        this.setState({
            isDragging: true,
            draggingIndex: index,
            draggingTargetIndex: index,
            draggingGrabbedOffset: draggingGrabbedOffset,
            top: top,
            left: left,
        });
    };
    ColumnEditCollection.prototype.renderGhost = function (gridColumns) {
        var _a, _b;
        var _c = this.state, isDragging = _c.isDragging, draggingIndex = _c.draggingIndex, draggingGrabbedOffset = _c.draggingGrabbedOffset;
        var index = draggingIndex;
        if (typeof index !== 'number' || !isDragging || !this.portal) {
            return null;
        }
        var dragOffsetX = (_a = draggingGrabbedOffset === null || draggingGrabbedOffset === void 0 ? void 0 : draggingGrabbedOffset.x) !== null && _a !== void 0 ? _a : 0;
        var dragOffsetY = (_b = draggingGrabbedOffset === null || draggingGrabbedOffset === void 0 ? void 0 : draggingGrabbedOffset.y) !== null && _b !== void 0 ? _b : 0;
        var top = Number(this.state.top) - dragOffsetY;
        var left = Number(this.state.left) - dragOffsetX;
        var col = this.props.columns[index];
        var style = {
            top: top + "px",
            left: left + "px",
        };
        var ghost = (<Ghost ref={this.dragGhostRef} style={style}>
        {this.renderItem(col, index, { isGhost: true, gridColumns: gridColumns })}
      </Ghost>);
        return react_dom_1.default.createPortal(ghost, this.portal);
    };
    ColumnEditCollection.prototype.renderItem = function (col, i, _a) {
        var _this = this;
        var _b = _a.canDelete, canDelete = _b === void 0 ? true : _b, _c = _a.canDrag, canDrag = _c === void 0 ? true : _c, _d = _a.isGhost, isGhost = _d === void 0 ? false : _d, _e = _a.gridColumns, gridColumns = _e === void 0 ? 2 : _e;
        var _f = this.props, columns = _f.columns, fieldOptions = _f.fieldOptions;
        var _g = this.state, isDragging = _g.isDragging, draggingTargetIndex = _g.draggingTargetIndex, draggingIndex = _g.draggingIndex;
        var placeholder = null;
        // Add a placeholder above the target row.
        if (isDragging && isGhost === false && draggingTargetIndex === i) {
            placeholder = (<DragPlaceholder key={"placeholder:" + this.keyForColumn(col, isGhost)} className={DRAG_CLASS}/>);
        }
        // If the current row is the row in the drag ghost return the placeholder
        // or a hole if the placeholder is elsewhere.
        if (isDragging && isGhost === false && draggingIndex === i) {
            return placeholder;
        }
        var position = Number(draggingTargetIndex) <= Number(draggingIndex)
            ? PlaceholderPosition.TOP
            : PlaceholderPosition.BOTTOM;
        return (<React.Fragment key={i + ":" + this.keyForColumn(col, isGhost)}>
        {position === PlaceholderPosition.TOP && placeholder}
        <RowContainer className={isGhost ? '' : DRAG_CLASS}>
          {canDrag ? (<button_1.default aria-label={locale_1.t('Drag to reorder')} onMouseDown={function (event) { return _this.startDrag(event, i); }} onTouchStart={function (event) { return _this.startDrag(event, i); }} icon={<icons_1.IconGrabbable size="xs"/>} size="zero" borderless/>) : (<span />)}
          <queryField_1.QueryField fieldOptions={fieldOptions} gridColumns={gridColumns} fieldValue={col} onChange={function (value) { return _this.handleUpdateColumn(i, value); }} error={this.state.error.get(i)} takeFocus={i === this.props.columns.length - 1} otherColumns={columns}/>
          {canDelete || col.kind === 'equation' ? (<button_1.default aria-label={locale_1.t('Remove column')} onClick={function () { return _this.removeColumn(i); }} icon={<icons_1.IconDelete />} borderless/>) : (<span />)}
        </RowContainer>
        {position === PlaceholderPosition.BOTTOM && placeholder}
      </React.Fragment>);
    };
    ColumnEditCollection.prototype.render = function () {
        var _this = this;
        var _a = this.props, className = _a.className, columns = _a.columns, organization = _a.organization;
        var canDelete = columns.filter(function (field) { return field.kind !== 'equation'; }).length > 1;
        var canDrag = columns.length > 1;
        var canAdd = columns.length < MAX_COL_COUNT;
        var title = canAdd
            ? undefined
            : "Sorry, you reached the maximum number of columns. Delete columns to add more.";
        // Get the longest number of columns so we can layout the rows.
        // We always want at least 2 columns.
        var gridColumns = Math.max.apply(Math, tslib_1.__spreadArray([], tslib_1.__read(columns.map(function (col) {
            return col.kind === 'function' && fields_1.AGGREGATIONS[col.function[0]].parameters.length === 2
                ? 3
                : 2;
        }))));
        return (<div className={className}>
        {this.renderGhost(gridColumns)}
        <RowContainer>
          <Heading gridColumns={gridColumns}>
            <StyledSectionHeading>{locale_1.t('Tag / Field / Function')}</StyledSectionHeading>
            <StyledSectionHeading>{locale_1.t('Field Parameter')}</StyledSectionHeading>
          </Heading>
        </RowContainer>
        {columns.map(function (col, i) {
                return _this.renderItem(col, i, { canDelete: canDelete, canDrag: canDrag, gridColumns: gridColumns });
            })}
        <RowContainer>
          <Actions>
            <button_1.default size="small" label={locale_1.t('Add a Column')} onClick={this.handleAddColumn} title={title} disabled={!canAdd} icon={<icons_1.IconAdd isCircled size="xs"/>}>
              {locale_1.t('Add a Column')}
            </button_1.default>
            <feature_1.default organization={organization} features={['discover-arithmetic']}>
              <button_1.default size="small" label={locale_1.t('Add an Equation')} onClick={this.handleAddEquation} title={title} disabled={!canAdd} icon={<icons_1.IconAdd isCircled size="xs"/>}>
                {locale_1.t('Add an Equation')}
                <StyledFeatureBadge type="new"/>
              </button_1.default>
            </feature_1.default>
          </Actions>
        </RowContainer>
      </div>);
    };
    return ColumnEditCollection;
}(React.Component));
var StyledFeatureBadge = styled_1.default(featureBadge_1.default)(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  margin: -", " auto;\n  margin-left: ", ";\n"], ["\n  margin: -", " auto;\n  margin-left: ", ";\n"])), space_1.default(0.5), space_1.default(1));
var RowContainer = styled_1.default('div')(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  display: grid;\n  grid-template-columns: ", " 1fr ", ";\n  justify-content: center;\n  align-items: center;\n  width: 100%;\n  touch-action: none;\n  padding-bottom: ", ";\n"], ["\n  display: grid;\n  grid-template-columns: ", " 1fr ", ";\n  justify-content: center;\n  align-items: center;\n  width: 100%;\n  touch-action: none;\n  padding-bottom: ", ";\n"])), space_1.default(3), space_1.default(3), space_1.default(1));
var Ghost = styled_1.default('div')(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  background: ", ";\n  display: block;\n  position: absolute;\n  padding: ", "px;\n  border-radius: ", ";\n  box-shadow: 0 0 15px rgba(0, 0, 0, 0.15);\n  width: 710px;\n  opacity: 0.8;\n  cursor: grabbing;\n  padding-right: ", ";\n\n  & > ", " {\n    padding-bottom: 0;\n  }\n\n  & svg {\n    cursor: grabbing;\n  }\n"], ["\n  background: ", ";\n  display: block;\n  position: absolute;\n  padding: ", "px;\n  border-radius: ", ";\n  box-shadow: 0 0 15px rgba(0, 0, 0, 0.15);\n  width: 710px;\n  opacity: 0.8;\n  cursor: grabbing;\n  padding-right: ", ";\n\n  & > ", " {\n    padding-bottom: 0;\n  }\n\n  & svg {\n    cursor: grabbing;\n  }\n"])), function (p) { return p.theme.background; }, GHOST_PADDING, function (p) { return p.theme.borderRadius; }, space_1.default(2), RowContainer);
var DragPlaceholder = styled_1.default('div')(templateObject_4 || (templateObject_4 = tslib_1.__makeTemplateObject(["\n  margin: 0 ", " ", " ", ";\n  border: 2px dashed ", ";\n  border-radius: ", ";\n  height: 41px;\n"], ["\n  margin: 0 ", " ", " ", ";\n  border: 2px dashed ", ";\n  border-radius: ", ";\n  height: 41px;\n"])), space_1.default(3), space_1.default(1), space_1.default(3), function (p) { return p.theme.border; }, function (p) { return p.theme.borderRadius; });
var Actions = styled_1.default('div')(templateObject_5 || (templateObject_5 = tslib_1.__makeTemplateObject(["\n  grid-column: 2 / 3;\n\n  & button {\n    margin-right: ", ";\n  }\n"], ["\n  grid-column: 2 / 3;\n\n  & button {\n    margin-right: ", ";\n  }\n"])), space_1.default(1));
var Heading = styled_1.default('div')(templateObject_6 || (templateObject_6 = tslib_1.__makeTemplateObject(["\n  grid-column: 2 / 3;\n\n  /* Emulate the grid used in the column editor rows */\n  display: grid;\n  grid-template-columns: repeat(", ", 1fr);\n  grid-column-gap: ", ";\n"], ["\n  grid-column: 2 / 3;\n\n  /* Emulate the grid used in the column editor rows */\n  display: grid;\n  grid-template-columns: repeat(", ", 1fr);\n  grid-column-gap: ", ";\n"])), function (p) { return p.gridColumns; }, space_1.default(1));
var StyledSectionHeading = styled_1.default(styles_1.SectionHeading)(templateObject_7 || (templateObject_7 = tslib_1.__makeTemplateObject(["\n  margin: 0;\n"], ["\n  margin: 0;\n"])));
exports.default = ColumnEditCollection;
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6, templateObject_7;
//# sourceMappingURL=columnEditCollection.jsx.map