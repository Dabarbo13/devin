import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import '@testing-library/jest-dom';
import { MockedProvider, MockedResponse } from '@apollo/client/testing';
import ClinicalTrials from './ClinicalTrials'; // Adjust path if needed
import { GET_STUDIES_LIST, GET_PARTICIPANTS_FOR_STUDY } from '../graphql/queries'; // Adjust path
import { AuthProvider } from '../context/AuthContext'; // Needed if ClinicalTrials uses useAuth, though not directly visible in snippet
import { HashRouter as Router } from 'react-router-dom'; // For Link components if any

// Mock data
const mockStudiesData = [
  {
    id: '1', title: 'Study Alpha', protocolNumber: 'P001', status: 'active', phase: 'PHASE_1',
    therapeuticArea: 'Oncology', principalInvestigator: { id: 'pi1', firstName: 'Jane', lastName: 'Doe', email: 'jane@example.com' },
    sponsorName: 'Sponsor X', startDate: '2024-01-01', targetEnrollment: 100,
  },
  {
    id: '2', title: 'Study Beta', protocolNumber: 'P002', status: 'completed', phase: 'PHASE_2',
    therapeuticArea: 'Cardiology', principalInvestigator: { id: 'pi2', firstName: 'John', lastName: 'Smith', email: 'john@example.com' },
    sponsorName: 'Sponsor Y', startDate: '2023-01-01', targetEnrollment: 50,
  },
];

const mockParticipantsDataStudy1 = [
  { id: 'p1', participantId: 'SUB001', firstName: 'Alice', lastName: 'Wonder', status: 'enrolled', enrollmentDate: '2024-02-01' },
  { id: 'p2', participantId: 'SUB002', firstName: 'Bob', lastName: 'Builder', status: 'active', enrollmentDate: '2024-02-05' },
];

const mocks: MockedResponse[] = [
  {
    request: { query: GET_STUDIES_LIST },
    result: { data: { studies: mockStudiesData } },
  },
  {
    request: { query: GET_PARTICIPANTS_FOR_STUDY, variables: { studyId: '1' } },
    result: { data: { participants: mockParticipantsDataStudy1 } },
  },
  { // Mock for study 2 if needed for other tests, or an empty array
    request: { query: GET_PARTICIPANTS_FOR_STUDY, variables: { studyId: '2' } },
    result: { data: { participants: [] } },
  },
];

// Helper to render with providers
const renderWithProviders = (ui: React.ReactElement) => {
  return render(
    <Router> {/* Router for Link components, if any */}
      <MockedProvider mocks={mocks} addTypename={false}>
        {/* AuthProvider might be needed if any child component or hook relies on it */}
        {/* For now, assuming ClinicalTrials itself doesn't directly call useAuth for its core data fetching */}
        <AuthProvider> 
            {ui}
        </AuthProvider>
      </MockedProvider>
    </Router>
  );
};

describe('ClinicalTrials Component', () => {
  test('renders loading state for studies initially, then displays studies', async () => {
    renderWithProviders(<ClinicalTrials />);
    expect(screen.getByText(/loading studies.../i)).toBeInTheDocument();
    await waitFor(() => {
      expect(screen.getByText(/study alpha/i)).toBeInTheDocument();
      expect(screen.getByText(/study beta/i)).toBeInTheDocument();
    });
    // Check if the initial message for participants is there
    expect(screen.getByText(/please select a study to see its participants/i)).toBeInTheDocument();
  });

  test('fetches and displays participants when a study is clicked', async () => {
    renderWithProviders(<ClinicalTrials />);
    // Wait for studies to load
    await waitFor(() => expect(screen.getByText(/study alpha/i)).toBeInTheDocument());

    // Click on the first study card (Study Alpha)
    fireEvent.click(screen.getByText(/study alpha/i).closest('div[role="button"], button, .cursor-pointer') || screen.getByText(/study alpha/i)); // More robust selector

    // Check for participants loading state
    expect(screen.getByText(/loading participants.../i)).toBeInTheDocument();
    
    // Wait for participants to load
    await waitFor(() => {
      expect(screen.getByText(/alice/i)).toBeInTheDocument(); // Check for participant name
      expect(screen.getByText(/bob/i)).toBeInTheDocument();
    });
    expect(screen.queryByText(/please select a study to see its participants/i)).not.toBeInTheDocument();
  });
  
  test('shows error message if fetching studies fails', async () => {
    const errorMocks: MockedResponse[] = [
      { request: { query: GET_STUDIES_LIST }, error: new Error('Failed to fetch studies') },
    ];
    render(
      <Router>
        <MockedProvider mocks={errorMocks} addTypename={false}>
          <AuthProvider><ClinicalTrials /></AuthProvider>
        </MockedProvider>
      </Router>
    );
    expect(screen.getByText(/loading studies.../i)).toBeInTheDocument();
    await waitFor(() => {
      expect(screen.getByText(/error fetching studies: failed to fetch studies/i)).toBeInTheDocument();
    });
  });

  test('shows error message if fetching participants fails', async () => {
    const participantErrorMocks: MockedResponse[] = [
      { request: { query: GET_STUDIES_LIST }, result: { data: { studies: [mockStudiesData[0]] } } }, // Need at least one study to click
      { request: { query: GET_PARTICIPANTS_FOR_STUDY, variables: { studyId: '1' } }, error: new Error('Failed to fetch participants') },
    ];
     render(
      <Router>
        <MockedProvider mocks={participantErrorMocks} addTypename={false}>
          <AuthProvider><ClinicalTrials /></AuthProvider>
        </MockedProvider>
      </Router>
    );
    await waitFor(() => expect(screen.getByText(mockStudiesData[0].title)).toBeInTheDocument());
    fireEvent.click(screen.getByText(mockStudiesData[0].title).closest('div[role="button"], button, .cursor-pointer') || screen.getByText(mockStudiesData[0].title));
    
    await waitFor(() => {
      expect(screen.getByText(/error fetching participants: failed to fetch participants/i)).toBeInTheDocument();
    });
  });

  // Test for "Clear Selection" button
  test('clears selected study and participant list on "Clear Selection"', async () => {
    renderWithProviders(<ClinicalTrials />);
    await waitFor(() => expect(screen.getByText(/study alpha/i)).toBeInTheDocument());

    fireEvent.click(screen.getByText(/study alpha/i).closest('div[role="button"], button, .cursor-pointer') || screen.getByText(/study alpha/i));
    await waitFor(() => expect(screen.getByText(/alice/i)).toBeInTheDocument()); // Participants loaded

    const clearButton = screen.getByRole('button', { name: /clear selection/i });
    fireEvent.click(clearButton);

    await waitFor(() => {
      expect(screen.getByText(/please select a study to see its participants/i)).toBeInTheDocument();
    });
    expect(screen.queryByText(/alice/i)).not.toBeInTheDocument(); // Participants should be cleared
  });

});
