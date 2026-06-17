import { useState, type FC } from 'react';
import Icon from '@plone/volto/components/theme/Icon/Icon';
import deleteSVG from '@plone/volto/icons/delete.svg';
import downloadSVG from '@plone/volto/icons/download.svg';
import { useIntl } from 'react-intl';
import { Button, Confirm } from 'semantic-ui-react';
import { messages } from './messages';

interface DataTableActionsProps {
  /** Number of stored submissions, shown in the results summary. */
  count: number;
  /** Triggered when the export button is pressed. */
  onExport: () => void;
  /** Triggered when the clear action is confirmed. */
  onClear: () => void;
}

/**
 * The DataTable toolbar: stored-item count plus export and clear actions.
 */
const DataTableActions: FC<DataTableActionsProps> = ({
  count,
  onExport,
  onClear,
}) => {
  const intl = useIntl();
  const [confirmOpen, setConfirmOpen] = useState(false);

  return (
    <div className="dt-wrapper-header">
      {/* RESULTS INFO */}
      <div className="dt-info-results">
        <p>
          <strong>{count} </strong>
          {count === 1
            ? intl.formatMessage(messages.formDataCountSingle)
            : intl.formatMessage(messages.formDataCount)}
        </p>
      </div>

      <div className="dt-actions">
        {/* BUTTON EXPORT */}
        <Button icon primary onClick={onExport}>
          <Icon name={downloadSVG} size="30px" />
          {intl.formatMessage(messages.exportCsv)}
        </Button>
        {/* BUTTON DELETE */}
        <Button icon negative onClick={() => setConfirmOpen(true)}>
          <Icon name={deleteSVG} size="30px" />
          {intl.formatMessage(messages.clearData)}
        </Button>
        {/* MODAL CONFIRM DELETE */}
        <Confirm
          open={confirmOpen}
          content={intl.formatMessage(messages.confirmClearData)}
          cancelButton={intl.formatMessage(messages.cancel)}
          onCancel={() => setConfirmOpen(false)}
          onConfirm={() => {
            onClear();
            setConfirmOpen(false);
          }}
        />
      </div>
    </div>
  );
};

export default DataTableActions;
