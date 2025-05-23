import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import '@testing-library/jest-dom';
import { MockedProvider, MockedResponse } from '@apollo/client/testing';
import AddStudyForm from './AddStudyForm'; // Adjust path if needed
import { CREATE_STUDY_MUTATION } from '../graphql/mutations'; // Adjust path
import { GET_STUDIES_LIST } from '../graphql/queries'; // For refetchQueries array

// Mock props
const mockOnClose = jest.fn();
const mockOnStudyAdded = jest.fn();

// Default input for successful mutation, closely matching form's cleanedStudyData
const defaultSuccessInput = { 
  title: 'New Test Study',
  protocolNumber: 'NTS001',
  description: 'A detailed description.',
  status: 'draft', // Default status in form
  phase: 'PHASE_1',
  therapeuticArea: 'Oncology',
  indication: 'Cancer',
  sponsorName: 'Test Sponsor Inc.',
  principalInvestigator: 'drtest@example.com',
  startDate: '2024-07-01',
  endDate: '2025-07-01',
  targetEnrollment: 150,
  isPublic: false, // Default isPublic in form
};

const mocks: MockedResponse[] = [
  {
    request: {
      query: CREATE_STUDY_MUTATION,
      variables: {
        input: defaultSuccessInput,
      },
    },
    result: {
      data: {
        createStudy: {
          study: { // This is the data expected by onStudyAdded
            id: '3', 
            title: 'New Test Study', 
            protocolNumber: 'NTS001', 
            status: 'draft', 
            phase: 'PHASE_1',
            description: 'A detailed description.', 
            therapeuticArea: 'Oncology', 
            indication: 'Cancer',
            principalInvestigator: { id: 'pi3', email: 'drtest@example.com', firstName: 'Dr', lastName: 'Test' },
            sponsorName: 'Test Sponsor Inc.', 
            startDate: '2024-07-01', 
            endDate: '2025-07-01',
            targetEnrollment: 150, 
            isPublic: false,
          },
        },
      },
    },
  },
  // Mock for refetchQueries: GET_STUDIES_LIST
  // This is important if your component relies on the list being updated immediately
  // or if Apollo Client strictness in tests requires all operations to be mocked.
  {
    request: { query: GET_STUDIES_LIST },
    result: { data: { studies: [] } } // Mocked empty or some representative list
  }
];


// Helper to render with providers
const renderWithProviders = (ui: React.ReactElement, customMocks?: MockedResponse[]) => {
  return render(
    <MockedProvider mocks={customMocks || mocks} addTypename={false}>
      {ui}
    </MockedProvider>
  );
};

describe('AddStudyForm Component', () => {
  beforeEach(() => {
    mockOnClose.mockClear();
    mockOnStudyAdded.mockClear();
  });

  test('renders all form fields correctly', () => {
    renderWithProviders(<AddStudyForm onClose={mockOnClose} onStudyAdded={mockOnStudyAdded} />);
    expect(screen.getByLabelText(/title/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/protocol number/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/description/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/status/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/phase/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/therapeutic area/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/indication/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/sponsor name/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/principal investigator \(email\)/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/start date/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/end date/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/target enrollment/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/is publicly visible\?/i)).toBeInTheDocument();
    
    expect(screen.getByRole('button', { name: /save study/i })).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /cancel/i })).toBeInTheDocument();
  });

  test('allows typing in text input fields', () => {
    renderWithProviders(<AddStudyForm onClose={mockOnClose} onStudyAdded={mockOnStudyAdded} />);
    
    const titleInput = screen.getByLabelText(/title/i);
    fireEvent.change(titleInput, { target: { value: 'My Study Title' } });
    expect(titleInput).toHaveValue('My Study Title');
    
    const protocolInput = screen.getByLabelText(/protocol number/i);
    fireEvent.change(protocolInput, { target: { value: 'PN123' } });
    expect(protocolInput).toHaveValue('PN123');
  });

  test('calls mutation, onStudyAdded, and onClose on successful submission', async () => {
    renderWithProviders(<AddStudyForm onClose={mockOnClose} onStudyAdded={mockOnStudyAdded} />);

    // Fill out the form to match defaultSuccessInput
    fireEvent.change(screen.getByLabelText(/title/i), { target: { value: 'New Test Study' } });
    fireEvent.change(screen.getByLabelText(/protocol number/i), { target: { value: 'NTS001' } });
    fireEvent.change(screen.getByLabelText(/description/i), { target: { value: 'A detailed description.' } });
    
    // For Select components, we need to simulate selection if the default isn't what we need.
    // Status defaults to 'draft' in the form, which matches our mock.
    // For Phase, the form defaults to '', but our mock expects 'PHASE_1'.
    // This simplified test will assume 'PHASE_1' is selected or set it.
    // For robust select testing:
    fireEvent.mouseDown(screen.getByLabelText(/phase/i)); // Assuming this targets the SelectTrigger
    await waitFor(() => screen.getByText('PHASE 1')); // Wait for item to be available
    fireEvent.click(screen.getByText('PHASE 1')); // Select the phase
    // We need to ensure the value selected for Phase matches the `defaultSuccessInput.phase`

    fireEvent.change(screen.getByLabelText(/therapeutic area/i), { target: { value: 'Oncology' } });
    fireEvent.change(screen.getByLabelText(/indication/i), { target: { value: 'Cancer' } });
    fireEvent.change(screen.getByLabelText(/sponsor name/i), { target: { value: 'Test Sponsor Inc.' } });
    fireEvent.change(screen.getByLabelText(/principal investigator \(email\)/i), { target: { value: 'drtest@example.com' } });
    fireEvent.change(screen.getByLabelText(/start date/i), { target: { value: '2024-07-01' } });
    fireEvent.change(screen.getByLabelText(/end date/i), { target: { value: '2025-07-01' } });
    fireEvent.change(screen.getByLabelText(/target enrollment/i), { target: { value: '150' } });
    // isPublic is false by default in the form, matching mock.

    fireEvent.click(screen.getByRole('button', { name: /save study/i }));

    await waitFor(() => {
      expect(mockOnStudyAdded).toHaveBeenCalledWith(mocks[0].result?.data?.createStudy.study);
    }, { timeout: 3000 }); // Increased timeout for safety
    await waitFor(() => {
      expect(mockOnClose).toHaveBeenCalled();
    }, { timeout: 1000 });
  });

  test('shows error message on mutation failure', async () => {
    const errorInput = { 
        title: 'Fail Study', protocolNumber: 'FS001', description: '', status: 'draft', phase: null,
        therapeuticArea: null, indication: null, sponsorName: null, principalInvestigator: null,
        startDate: null, endDate: null, targetEnrollment: null, isPublic: false 
    };
    const errorMocks: MockedResponse[] = [
      {
        request: { query: CREATE_STUDY_MUTATION, variables: { input: errorInput } },
        error: new Error('Network Error: Failed to create study'),
      },
       // It's good practice to also mock refetchQueries if the mutation triggers them, even on error path,
       // though they might not be called if the mutation itself errors out before onCompleted.
      {
        request: { query: GET_STUDIES_LIST },
        result: { data: { studies: [] } } 
      }
    ];
    renderWithProviders(<AddStudyForm onClose={mockOnClose} onStudyAdded={mockOnStudyAdded} />, errorMocks);

    fireEvent.change(screen.getByLabelText(/title/i), { target: { value: 'Fail Study' } });
    fireEvent.change(screen.getByLabelText(/protocol number/i), { target: { value: 'FS001' } });
    // Other fields will use their defaults or empty strings which become nulls, matching errorInput.
    
    fireEvent.click(screen.getByRole('button', { name: /save study/i }));

    await waitFor(() => {
      // The error message displayed comes from mutationError.message
      expect(screen.getByText(/failed to add study: network error: failed to create study/i)).toBeInTheDocument();
    });
    expect(mockOnStudyAdded).not.toHaveBeenCalled();
    expect(mockOnClose).not.toHaveBeenCalled(); // onClose is typically not called on error
  });
  
  test('calls onClose when Cancel button is clicked', () => {
    renderWithProviders(<AddStudyForm onClose={mockOnClose} onStudyAdded={mockOnStudyAdded} />);
    fireEvent.click(screen.getByRole('button', { name: /cancel/i }));
    expect(mockOnClose).toHaveBeenCalled();
  });

});
