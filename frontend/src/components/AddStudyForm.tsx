import React, { useState } from 'react';
import { Button } from './ui/button';
import { Input } from './ui/input';
import { Label } from './ui/label';
import { Textarea } from './ui/textarea';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from './ui/select';
import { Switch } from './ui/switch';
import { ScrollArea } from './ui/scroll-area';
import { useMutation } from '@apollo/client'; // Added
import { CREATE_STUDY_MUTATION } from '../graphql/mutations'; // Added
import { GET_STUDIES_LIST } from '../graphql/queries'; // Added for refetch

// Define choices based on backend Study model
const STATUS_CHOICES = ['draft', 'pending_approval', 'approved', 'active', 'paused', 'completed', 'terminated'];
const PHASE_CHOICES = ['PHASE_0', 'PHASE_1', 'PHASE_2', 'PHASE_3', 'PHASE_4'];

interface AddStudyFormProps {
  onClose: () => void;
  onStudyAdded: (newStudyData: any) => void; // Callback after study is added
}

const AddStudyForm: React.FC<AddStudyFormProps> = ({ onClose, onStudyAdded }) => {
  const [title, setTitle] = useState('');
  const [protocolNumber, setProtocolNumber] = useState('');
  const [description, setDescription] = useState('');
  const [status, setStatus] = useState('draft');
  const [phase, setPhase] = useState('');
  const [therapeuticArea, setTherapeuticArea] = useState('');
  const [indication, setIndication] = useState('');
  const [sponsorName, setSponsorName] = useState('');
  const [principalInvestigatorEmail, setPrincipalInvestigatorEmail] = useState(''); 
  const [startDate, setStartDate] = useState('');
  const [endDate, setEndDate] = useState('');
  const [targetEnrollment, setTargetEnrollment] = useState('');
  const [isPublic, setIsPublic] = useState(false);

  const [createStudy, { loading: mutationLoading, error: mutationError }] = useMutation(
    CREATE_STUDY_MUTATION,
    {
      refetchQueries: [{ query: GET_STUDIES_LIST }],
      onCompleted: (data) => {
        if (data && data.createStudy && data.createStudy.study) {
          onStudyAdded(data.createStudy.study);
        }
        onClose(); // Close form on success
      },
      onError: (err) => {
        console.error("Failed to create study:", err);
        // The error will be displayed via mutationError in the JSX
      }
    }
  );

  const handleSubmit = async (event: React.FormEvent) => {
    event.preventDefault();

    const studyData = {
      title,
      protocolNumber,
      description,
      status,
      phase: phase === "" ? null : phase,
      therapeuticArea: therapeuticArea || null,
      indication: indication || null,
      sponsorName: sponsorName || null,
      // This field name 'principalInvestigator' must match the expected field in StudyInput type in GraphQL schema.
      // If the backend expects an ID, this needs to be handled (e.g., by looking up user by email or providing a selector).
      // Assuming 'principalInvestigator' can be an email string that backend resolves, or it's a placeholder for an ID.
      principalInvestigator: principalInvestigatorEmail || null, 
      startDate: startDate || null,
      endDate: endDate || null,
      targetEnrollment: targetEnrollment ? parseInt(targetEnrollment, 10) : null,
      isPublic,
    };
    
    // Filter out null values if your backend schema doesn't expect them for optional fields.
    // Graphene/Django usually handles null for non-required fields gracefully if `required=False`.
    // If any field is explicitly non-nullable and optional, it might expect 'undefined' or the field to be absent.
    // For this example, we'll send nulls for optional fields if they are empty.
    const cleanedStudyData: { [key: string]: any } = {};
    for (const [key, value] of Object.entries(studyData)) {
      if (value !== null && value !== '') { // Keep empty strings if backend expects them, otherwise filter
        cleanedStudyData[key] = value;
      } else if (value === null) { // Explicitly send nulls if they are set
         cleanedStudyData[key] = null;
      }
    }
    // Ensure targetEnrollment is an int or null
    if (cleanedStudyData.targetEnrollment === undefined && studyData.targetEnrollment === null) {
        cleanedStudyData.targetEnrollment = null;
    } else if (targetEnrollment === '') { // If user cleared the field
        cleanedStudyData.targetEnrollment = null;
    }

    // Ensure boolean isPublic is always present
    cleanedStudyData.isPublic = isPublic;


    try {
      console.log('Submitting cleaned study data:', cleanedStudyData);
      await createStudy({ variables: { input: cleanedStudyData } });
      // onCompleted will handle success actions like closing the form and calling onStudyAdded
    } catch (err) {
      // Error is captured by useMutation's error state (mutationError)
      // Additional logging if needed, but UI display is handled by mutationError
      console.error("Error during createStudy mutation call in handleSubmit:", err);
    }
  };

  return (
    <ScrollArea className="h-[calc(100vh-100px)]"> 
      <form onSubmit={handleSubmit} className="space-y-4 p-6">
        <h2 className="text-xl font-semibold mb-4">Add New Clinical Study</h2>
        
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <Label htmlFor="titleAddForm">Title</Label>
            <Input id="titleAddForm" value={title} onChange={(e) => setTitle(e.target.value)} required disabled={mutationLoading} />
          </div>
          <div>
            <Label htmlFor="protocolNumberAddForm">Protocol Number</Label>
            <Input id="protocolNumberAddForm" value={protocolNumber} onChange={(e) => setProtocolNumber(e.target.value)} required disabled={mutationLoading} />
          </div>
        </div>

        <div>
          <Label htmlFor="descriptionAddForm">Description</Label>
          <Textarea id="descriptionAddForm" value={description} onChange={(e) => setDescription(e.target.value)} disabled={mutationLoading} />
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <Label htmlFor="statusAddForm">Status</Label>
            <Select value={status} onValueChange={setStatus} disabled={mutationLoading}>
              <SelectTrigger><SelectValue placeholder="Select status" /></SelectTrigger>
              <SelectContent>
                {STATUS_CHOICES.map(s => <SelectItem key={s} value={s}>{s.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase())}</SelectItem>)}
              </SelectContent>
            </Select>
          </div>
          <div>
            <Label htmlFor="phaseAddForm">Phase</Label>
            <Select value={phase} onValueChange={setPhase} disabled={mutationLoading}>
              <SelectTrigger><SelectValue placeholder="Select phase" /></SelectTrigger>
              <SelectContent>
                <SelectItem value="">N/A</SelectItem>
                {PHASE_CHOICES.map(p => <SelectItem key={p} value={p}>{p.replace('_', ' ')}</SelectItem>)}
              </SelectContent>
            </Select>
          </div>
        </div>
        
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <Label htmlFor="therapeuticAreaAddForm">Therapeutic Area</Label>
            <Input id="therapeuticAreaAddForm" value={therapeuticArea} onChange={(e) => setTherapeuticArea(e.target.value)} disabled={mutationLoading} />
          </div>
          <div>
            <Label htmlFor="indicationAddForm">Indication</Label>
            <Input id="indicationAddForm" value={indication} onChange={(e) => setIndication(e.target.value)} disabled={mutationLoading} />
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <Label htmlFor="sponsorNameAddForm">Sponsor Name</Label>
            <Input id="sponsorNameAddForm" value={sponsorName} onChange={(e) => setSponsorName(e.target.value)} disabled={mutationLoading} />
          </div>
          <div>
            <Label htmlFor="principalInvestigatorEmailAddForm">Principal Investigator (Email)</Label>
            <Input id="principalInvestigatorEmailAddForm" type="email" value={principalInvestigatorEmail} onChange={(e) => setPrincipalInvestigatorEmail(e.target.value)} placeholder="pi@example.com" disabled={mutationLoading} />
          </div>
        </div>
        
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <Label htmlFor="startDateAddForm">Start Date</Label>
            <Input id="startDateAddForm" type="date" value={startDate} onChange={(e) => setStartDate(e.target.value)} disabled={mutationLoading} />
          </div>
          <div>
            <Label htmlFor="endDateAddForm">End Date</Label>
            <Input id="endDateAddForm" type="date" value={endDate} onChange={(e) => setEndDate(e.target.value)} disabled={mutationLoading} />
          </div>
        </div>

        <div>
          <Label htmlFor="targetEnrollmentAddForm">Target Enrollment</Label>
          <Input id="targetEnrollmentAddForm" type="number" value={targetEnrollment} onChange={(e) => setTargetEnrollment(e.target.value)} disabled={mutationLoading} />
        </div>

        <div className="flex items-center space-x-2">
          <Switch id="isPublicAddForm" checked={isPublic} onCheckedChange={setIsPublic} disabled={mutationLoading} />
          <Label htmlFor="isPublicAddForm">Is Publicly Visible?</Label>
        </div>

        {mutationError && <p className="text-sm text-red-600">Failed to add study: {mutationError.message}</p>}

        <div className="flex justify-end space-x-2 pt-4">
          <Button type="button" variant="outline" onClick={onClose} disabled={mutationLoading}>Cancel</Button>
          <Button type="submit" disabled={mutationLoading}>
            {mutationLoading ? 'Saving...' : 'Save Study'}
          </Button>
        </div>
      </form>
    </ScrollArea>
  );
};

export default AddStudyForm;
