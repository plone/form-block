import { defineMessages, injectIntl } from 'react-intl';
import type { IntlShape } from 'react-intl';

import { getInnerWidget } from '@plone/volto-form-block/helpers/schema';
import FormFieldWrapper from '@plone/volto-form-block/components/Wrappers/FormFieldWrapper';

const messages = defineMessages({
  required: {
    id: 'form_required',
    defaultMessage: 'Required',
  },
});

type NumberWrapperProps = {
  id: string;
  title: string;
  description?: string;
  required?: boolean;
  error?: string[];
  value?: string;
  onChange: (id: string, value?: string) => void;
  onClick: () => void;
  placeholder?: string;
  isDisabled?: boolean;
  intl: IntlShape;
};

const NumberWrapper = (props: NumberWrapperProps) => {
  const {
    id,
    value,
    onChange,
    onClick,
    placeholder,
    isDisabled,
    title,
    description,
    required,
    error,
    intl,
  } = props;

  const Widget = getInnerWidget('number');

  return (
    <FormFieldWrapper {...props} className="text">
      <Widget
        id={`field-${id}`}
        name={id}
        value={value || ''}
        label={title}
        description={description}
        type="number"
        isRequired={required}
        labelRequired={intl.formatMessage(messages.required)}
        disabled={isDisabled}
        placeholder={placeholder}
        onChange={(value) => onChange(id, value === '' ? undefined : value)}
        errorMessage={error ? error[0] : ''}
        isInvalid={error}
        onClick={() => onClick()}
      />
    </FormFieldWrapper>
  );
};

export default injectIntl(NumberWrapper);
