import { gql } from '@apollo/client';

export const GET_STUDIES_LIST = gql`
  query GetStudiesList {
    studies {
      id
      title
      protocolNumber
      status
      phase
      therapeuticArea
      principalInvestigator {
        id
        firstName
        lastName
        email
      }
      sponsorName
      startDate
      targetEnrollment
    }
  }
`;

export const GET_STUDY_DETAILS = gql`
  query GetStudyDetails($id: ID!) {
    study(id: $id) {
      id
      title
      protocolNumber
      description
      status
      phase
      therapeuticArea
      indication
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
      phases {
        id
        name
        description
        order
        phaseType
      }
      arms {
        id
        name
        description
        armType
      }
      # documents { id title documentType version }
      # sites { id name }
      # eligibilityCriteria { id description criteriaType }
    }
  }
`;

export const GET_PARTICIPANTS_FOR_STUDY = gql`
  query GetParticipantsForStudy($studyId: ID!) {
    participants(studyId: $studyId) {
      id
      participantId # From Participant model's participant_id field
      firstName
      lastName
      status
      # site { id name } # Placeholder if site is a nested object
      enrollmentDate
      # Other fields from ParticipantType as needed
    }
  }
`;
