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

type CheckboxWrapperProps = {
  id: string;
  title: string;
  description?: string;
  required?: boolean;
  error?: string[];
  value?: string;
  default?: string;
  onChange: (id: string, value?: string) => void;
  onClick: () => void;
  isDisabled?: boolean;
  intl: IntlShape;
};

const CheckboxWrapper = (props: CheckboxWrapperProps) => {
  const {
    id,
    value,
    onChange,
    onClick,
    isDisabled,
    title,
    description,
    required,
    error,
    intl,
  } = props;

  const Widget = getInnerWidget('checkbox');

  return (
    <FormFieldWrapper {...props} className="text">
      <Widget
        id={`field-${id}`}
        name={id}
        value={value || ''}
        label={title}
        description={description}
        default={props.default}
        isRequired={required}
        labelRequired={intl.formatMessage(messages.required)}
        disabled={isDisabled}
        onChange={(value) => onChange(id, value === '' ? undefined : value)}
        onClick={() => onClick()}
        errorMessage={error ? error[0] : ''}
        isInvalid={error !== undefined}
      />
    </FormFieldWrapper>
  );
};

export default injectIntl(CheckboxWrapper);
