import { defineMessages, injectIntl } from 'react-intl';
import type { IntlShape } from 'react-intl';
import isString from 'lodash/isString';
import map from 'lodash/map';

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

type CheckboxGroupWrapperProps = {
  id: string;
  title: string;
  description?: string;
  required?: boolean;
  error?: string[];
  value?: string | string[];
  default?: string | string[];
  choices?: [string, string][];
  onChange: (id: string, value?: string[]) => void;
  onClick: () => void;
  isDisabled?: boolean;
  intl: IntlShape;
};

const CheckboxGroupWrapper = (props: CheckboxGroupWrapperProps) => {
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

  const CheckboxGroup = getInnerWidget('checkboxGroup');
  const Checkbox = getInnerWidget('checkboxGroupOption');
  const Select = getInnerWidget('select');

  const options = choices || [];

  const curValue = value
    ? isString(value)
      ? value.split('\n')
      : value
    : undefined;

  const curDefault = props.default
    ? isString(props.default)
      ? props.default.split('\n')
      : props.default
    : undefined;

  return (
    <FormFieldWrapper {...props} className="text">
      {options.length < 6 && (
        <CheckboxGroup
          id={`field-${id}`}
          name={id}
          value={curValue || []}
          label={title}
          description={description}
          isRequired={required}
          labelRequired={intl.formatMessage(messages.required)}
          disabled={isDisabled}
          onChange={(value) => onChange(id, value)}
          errorMessage={error ? error[0] : ''}
          onClick={() => onClick()}
          isInvalid={error !== undefined}
        >
          {options.map((option) => (
            <Checkbox
              key={option}
              value={option[0]}
              isInvalid={error !== undefined}
            >
              {option[1]}
            </Checkbox>
          ))}
        </CheckboxGroup>
      )}
      {options.length > 5 && (
        <Select
          id={`field-${id}`}
          name={id}
          value={
            (curValue &&
              map(curValue, (item) => ({ value: item, label: item }))) ||
            (curDefault &&
              map(curDefault, (item) => ({
                value: item,
                label: item,
              }))) ||
            undefined
          }
          label={title}
          description={description}
          isRequired={required}
          isMulti={true}
          placeholder={intl.formatMessage(messages.select)}
          labelRequired={intl.formatMessage(messages.required)}
          disabled={isDisabled}
          onChange={(value) => {
            return onChange(
              id,
              map(value, (item) => item.value),
            );
          }}
          onClick={() => onClick()}
          options={options.map((option) => ({
            value: option[0],
            label: option[1],
          }))}
          errorMessage={error ? error[0] : ''}
          isInvalid={error}
        />
      )}
    </FormFieldWrapper>
  );
};

export default injectIntl(CheckboxGroupWrapper);
