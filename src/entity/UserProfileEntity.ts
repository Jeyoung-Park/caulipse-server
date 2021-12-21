import { Column, Entity, JoinColumn, OneToOne, PrimaryColumn } from 'typeorm';
import User from './UserEntity';

@Entity({ name: 'USER_PROFILE' })
export default class UserProfile {
  @PrimaryColumn('uuid')
  USER_ID!: string;

  @OneToOne(() => User, (user) => user.id)
  @JoinColumn({ name: 'USER_ID' })
  id!: User;

  @Column({ name: 'USER_NAME' })
  userName!: string;

  // FIXME: enum type으로 수정
  @Column({ name: 'DEPT' })
  dept!: string;

  // FIXME: enum type으로 수정
  @Column({ name: 'GRADE' })
  grade!: string;

  @Column({ name: 'BIO' })
  bio!: string;

  @Column({ name: 'USER_ABOUT' })
  userAbout!: string;

  @Column({ name: 'SHOW_DEPT' })
  showDept!: boolean;

  @Column({ name: 'SHOW_GRADE' })
  showGrade!: boolean;

  @Column({ name: 'ON_BREAK' })
  onBreak!: boolean;

  @Column({ name: 'EMAIL1' })
  email1!: string;

  @Column({ name: 'EMAIL2' })
  email2!: string;

  @Column({ name: 'EMAIL3' })
  email3!: string;

  @Column({ name: 'LINK1' })
  link1!: string;

  @Column({ name: 'LINK2' })
  link2!: string;
}
