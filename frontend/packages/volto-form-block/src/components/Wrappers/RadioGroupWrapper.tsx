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

type RadioGroupWrapperProps = {
  id: string;
  title: string;
  description?: string;
  required?: boolean;
  error?: string[];
  value?: string;
  choices?: [string, string][];
  onChange: (id: string, value?: string) => void;
  onClick: () => void;
  isDisabled?: boolean;
  intl: IntlShape;
};

const RadioGroupWrapper = (props: RadioGroupWrapperProps) => {
  const {
    id,
    value,
    choices,
    onChange,
    onClick,
    isDisabled,
    title,
    description,
    required,
    error,
    intl,
  } = props;

  const Widget = getInnerWidget('radioGroup');
  const OptionWidget = getInnerWidget('radioGroupOption');

  const options = choices || [];

  return (
    <FormFieldWrapper {...props} className="text">
      <Widget
        id={`field-${id}`}
        name={id}
        value={value || undefined}
        label={title}
        description={description}
        isRequired={required}
        labelRequired={intl.formatMessage(messages.required)}
        disabled={isDisabled}
        onChange={(value) => onChange(id, value === '' ? undefined : value)}
        onClick={() => onClick()}
        errorMessage={error ? error[0] : ''}
        isInvalid={error}
      >
        {options.map((option) => (
          <OptionWidget key={option[0]} value={option[0]}>
            {option[1]}
          </OptionWidget>
        ))}
      </Widget>
    </FormFieldWrapper>
  );
};

export default injectIntl(RadioGroupWrapper);
