import { gql } from '@apollo/client';

export const CREATE_STUDY_MUTATION = gql`
  mutation CreateStudy($input: StudyInput!) {
    createStudy(input: $input) {
      study {
        id
        title
        protocolNumber
        status
        phase
        description # Added description as it's in the form
        therapeuticArea
        indication
        # Assuming principalInvestigator in StudyInput might take an ID or an email
        # The backend CreateStudy resolver handles PI logic.
        # For now, the form sends principalInvestigatorEmail as 'principalInvestigator'.
        # The response structure for PI might be different, adjust if needed.
        principalInvestigator {
          id
          firstName
          lastName
          email
        }
        sponsorName
        startDate
        endDate
        targetEnrollment
        isPublic
      }
    }
  }
`;
