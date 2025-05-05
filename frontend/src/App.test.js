import { render, screen } from '@testing-library/react';
import App from './App';

test('renders Microservice Frontend heading', () => {
  render(<App />);
  const heading = screen.getByText(/Microservice Frontend/i);
  expect(heading).toBeInTheDocument();
});
