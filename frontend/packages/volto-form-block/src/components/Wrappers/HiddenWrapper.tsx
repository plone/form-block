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

type HiddenWrapperProps = {
  id: string;
  title: string;
  description?: string;
  required?: boolean;
  error?: string[];
  value?: string;
  onChange: (id: string, value?: string) => void;
  onClick: () => void;
  onEdit?: (id: string) => void;
  placeholder?: string;
  isDisabled?: boolean;
  intl: IntlShape;
};

const HiddenWrapper = (props: HiddenWrapperProps) => {
  const {
    id,
    value,
    onChange,
    onClick,
    placeholder,
    isDisabled,
    title,
    description,
    onEdit,
    required,
    error,
    intl,
  } = props;

  const Widget = getInnerWidget('hidden');

  return onEdit ? (
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
        placeholder={placeholder}
        onChange={(value) => onChange(id, value === '' ? undefined : value)}
        onClick={() => onClick()}
        errorMessage={error ? error[0] : ''}
        isInvalid={error}
      />
    </FormFieldWrapper>
  ) : (
    <input
      id={`field-${id}`}
      name={id}
      value={value || ''}
      placeholder={placeholder}
      type="hidden"
    />
  );
};

export default injectIntl(HiddenWrapper);
