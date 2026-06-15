import { defineMessages, injectIntl } from 'react-intl';
import type { IntlShape } from 'react-intl';

import { getInnerWidget } from '@plone/volto-form-block/helpers/schema';
import FormFieldWrapper from '@plone/volto-form-block/components/Wrappers/FormFieldWrapper';

const messages = defineMessages({
  required: {
    id: 'form_required',
    defaultMessage: 'Required',
  },
  select: {
    id: 'select',
    defaultMessage: 'Select...',
  },
});

type SelectWrapperProps = {
  id: string;
  title: string;
  description?: string;
  required?: boolean;
  error?: string[];
  value?: string;
  default?: string;
  choices?: [string, string][];
  onChange: (id: string, value?: string) => void;
  onClick: () => void;
  isDisabled?: boolean;
  intl: IntlShape;
};

const SelectWrapper = (props: SelectWrapperProps) => {
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

  const Widget = getInnerWidget('select');

  const options = choices || [];

  return (
    <FormFieldWrapper {...props} className="select">
      <Widget
        id={`field-${id}`}
        name={id}
        value={
          (value && { value, label: value }) ||
          (props.default && { value: props.default, label: props.default }) ||
          undefined
        }
        label={title}
        description={description}
        isRequired={required}
        labelRequired={intl.formatMessage(messages.required)}
        disabled={isDisabled}
        placeholder={intl.formatMessage(messages.select)}
        onChange={(value) => onChange(id, value.value)}
        errorMessage={error ? error[0] : ''}
        isInvalid={error}
        onClick={() => onClick()}
        options={options.map((option) => ({
          value: option[0],
          label: option[1],
        }))}
      />
    </FormFieldWrapper>
  );
};

export default injectIntl(SelectWrapper);
