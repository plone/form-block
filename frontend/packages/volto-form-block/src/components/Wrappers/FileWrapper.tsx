import { readAsDataURL } from 'promise-file-reader';
import { defineMessages, injectIntl } from 'react-intl';
import type { IntlShape } from 'react-intl';

import { getInnerWidget } from '@plone/volto-form-block/helpers/schema';
import FormFieldWrapper from '@plone/volto-form-block/components/Wrappers/FormFieldWrapper';

const messages = defineMessages({
  required: {
    id: 'form_required',
    defaultMessage: 'Required',
  },
  no_file: {
    id: 'no_file',
    defaultMessage: 'No file chosen',
  },
  choose_file: {
    id: 'choose_file',
    defaultMessage: 'Choose file',
  },
});

type FileValue = {
  data: string;
  encoding: string;
  'content-type': string;
  filename: string;
  size: number;
};

type FileWrapperProps = {
  id: string;
  title: string;
  description?: string;
  required?: boolean;
  error?: string[];
  value?: FileValue | null;
  onChange: (id: string, value: FileValue | null) => void;
  accept?: string;
  size?: string | number;
  isDisabled?: boolean;
  intl: IntlShape;
};

const FileWrapper = (props: FileWrapperProps) => {
  const {
    id,
    value,
    onChange,
    isDisabled,
    title,
    description,
    accept,
    size,
    required,
    error,
    intl,
  } = props;

  const Widget = getInnerWidget('file');

  return (
    <FormFieldWrapper {...props} className="text">
      <Widget
        id={`field-${id}`}
        name={id}
        labelFile={value?.filename || intl.formatMessage(messages.no_file)}
        label={title}
        labelButton={intl.formatMessage(messages.choose_file)}
        description={description}
        isRequired={required}
        labelRequired={intl.formatMessage(messages.required)}
        disabled={isDisabled}
        accept={accept}
        size={size}
        onSelect={(files: File[]) => {
          if (files.length < 1) return;
          const file = files[0];
          readAsDataURL(file).then((data: string) => {
            const fields = data.match(/^data:(.*);(.*),(.*)$/);
            if (!fields) return;
            onChange(id, {
              data: fields[3],
              encoding: fields[2],
              'content-type': fields[1],
              filename: file.name,
              size: file.size,
            });
          });
        }}
        deleteFilesCallback={() => {
          onChange(id, null);
        }}
        errorMessage={error ? error[0] : ''}
        hasError={error}
        isInvalid={error}
      />
    </FormFieldWrapper>
  );
};

export default injectIntl(FileWrapper);
