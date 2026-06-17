import type { ReactNode } from 'react';
import type { IntlShape } from 'react-intl';
import { messages } from './messages';

/**
 * Render a stored field value according to its field type.
 *
 * :param fieldType: The stored field's ``field_type`` (e.g. ``attachment``).
 * :param value: The stored value for the cell.
 * :param intl: The active react-intl shape, used for localized labels.
 * :returns: The cell content.
 */
export function renderStoredFieldCell(
  fieldType: string | undefined,
  value: any,
  intl: IntlShape,
): ReactNode {
  switch (fieldType) {
    case 'attachment':
      // TODO: unused fields:
      // value.size -> size in bytes
      // value.contentType -> mime type
      return value ? (
        <a href={value.url} download>
          {value.filename}
        </a>
      ) : (
        ''
      );
    case 'textarea':
      return <pre>{value || ''}</pre>;
    case 'checkbox':
      return value
        ? intl.formatMessage(messages.formValueYes)
        : intl.formatMessage(messages.formValueNo);
    default:
      return value || '';
  }
}
