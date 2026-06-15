import { defineMessages, injectIntl } from 'react-intl';
import type { IntlShape } from 'react-intl';

import {
  serializeDateValue,
  parseDateValue,
  type DateValue,
} from '@plone/volto-form-block/helpers/date';
import { getInnerWidget } from '@plone/volto-form-block/helpers/schema';
import FormFieldWrapper from '@plone/volto-form-block/components/Wrappers/FormFieldWrapper';

const messages = defineMessages({
  required: {
    id: 'form_required',
    defaultMessage: 'Required',
  },
});

type DatetimeWrapperProps = {
  id: string;
  title: string;
  description?: string;
  required?: boolean;
  error?: string[];
  value?: string;
  widget?: string;
  onChange: (id: string, value?: string) => void;
  onClick: () => void;
  isDisabled?: boolean;
  intl: IntlShape;
};

const DatetimeWrapper = (props: DatetimeWrapperProps) => {
  const {
    id,
    value,
    onChange,
    onClick,
    isDisabled,
    title,
    description,
    widget,
    required,
    error,
    intl,
  } = props;

  const Widget = getInnerWidget('datetime');
  const onDateChange = (date: DateValue | null) => {
    onChange(
      id,
      date ? serializeDateValue(date, widget === 'date') : undefined,
    );
  };

  const dateValue = value ? parseDateValue(value, widget === 'date') : null;

  return (
    <FormFieldWrapper {...props} className="text">
      <Widget
        id={`field-${id}`}
        name={id}
        value={dateValue}
        label={title}
        locale={intl.locale}
        description={description}
        isRequired={required}
        labelRequired={intl.formatMessage(messages.required)}
        disabled={isDisabled}
        isDateOnly={widget === 'date'}
        onChange={onDateChange}
        onChangeTime={onDateChange}
        onClick={() => onClick()}
        errorMessage={error ? error[0] : ''}
        isInvalid={error}
      />
    </FormFieldWrapper>
  );
};

export default injectIntl(DatetimeWrapper);
