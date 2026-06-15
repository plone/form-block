import type { ReactNode, FormEvent } from 'react';
import _ from 'lodash';

type FormComponentProps = {
  children?: ReactNode;
  onSubmit?: (...args: unknown[]) => void;
  error?: boolean;
};

const FormComponent = (props: FormComponentProps) => {
  const { children, error } = props;

  const handleSubmit = (e: FormEvent, ...args: unknown[]) => {
    _.invoke(e, 'preventDefault');
    _.invoke(props, 'onSubmit', e, props, ...args);
  };

  return (
    <form onSubmit={handleSubmit} className={error ? 'error' : ''}>
      {children}
    </form>
  );
};

export default FormComponent;
