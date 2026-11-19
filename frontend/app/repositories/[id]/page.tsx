import { RepositoryDetails } from "../../../components/repository-details";

export default async function RepositoryPage({ params }: { params: Promise<{ id: string }> }) {
  const { id } = await params;
  return <RepositoryDetails repositoryId={Number(id)} />;
}
