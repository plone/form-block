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

type EmailWrapperProps = {
  id: string;
  title: string;
  description?: string;
  required?: boolean;
  error?: string[];
  value?: string;
  onChange: (id: string, value?: string) => void;
  onClick: () => void;
  minLength?: string;
  maxLength?: string;
  isDisabled?: boolean;
  intl: IntlShape;
};

const EmailWrapper = (props: EmailWrapperProps) => {
  const {
    id,
    value,
    onChange,
    onClick,
    minLength,
    maxLength,
    isDisabled,
    title,
    description,
    required,
    error,
    intl,
  } = props;

  const Widget = getInnerWidget('email');

  return (
    <FormFieldWrapper {...props} className="text">
      <Widget
        id={`field-${id}`}
        name={id}
        value={value || ''}
        label={title}
        description={description}
        isRequired={required}
        labelRequired={intl.formatMessage(messages.required)}
        disabled={isDisabled}
        type="email"
        onChange={(value) => onChange(id, value === '' ? undefined : value)}
        onClick={() => onClick()}
        minLength={minLength || null}
        maxLength={maxLength || null}
        errorMessage={error ? error[0] : ''}
        isInvalid={error}
      />
    </FormFieldWrapper>
  );
};

export default injectIntl(EmailWrapper);
